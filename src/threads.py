import asyncio
from enum import Enum, auto
from io import BytesIO
from math import ceil
import ssl
from time import perf_counter
import aiohttp
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from constants import Constants
from utilities import checksum_ok
from web_utilities import (
    get_cacert_file,
    get_pool_manager,
)
# Needed for pyinstaller compilation.
import encodings.idna  # noqa: 401


class ThreadStatus(Enum):
    """Possible thread status."""

    OK                = auto()
    NO_CONNECTION_ERR = auto()
    UNKNOWN_ERR       = auto()
    BAD_DOWNLOAD_ERR  = auto()
    UNDEFINED         = auto()
    SLOW_CONN_ERR     = auto()


class _SlowConnError(Exception):
    pass


class BaseDownloadThread(QThread):
    """Subclass QThread. Base class for the download threads."""

    def __init__(self, parent=None):
        """Set the status to 'UNDEFINED'."""
        super().__init__(parent)
        self.status = ThreadStatus.UNDEFINED

    # def __del__(self):
    #     """Force the termination of the thread."""
    #     self.terminate()
    #     self.wait()


class DownloadThread(BaseDownloadThread):
    """Subclass BaseDownloadThread. Download the database folder. Used also for software updates."""

    progress = pyqtSignal(int)
    speed_progress = pyqtSignal(float)
    _CHUNK = 128 * 1024
    _DELTAT = 2

    def __init__(self, min_bytes=1024**2):
        """Just call super().__init__."""
        super().__init__()
        self._min_bytes = min_bytes
        self._data = None
        self._exit_call = False
        self._target = None

    def _pretty_len(self, byte_obj):
        """Return a well-formatted number of downloaded MB."""
        mega = len(byte_obj) / self._min_bytes
        if mega.is_integer():
            return int(mega)
        else:
            return ceil(mega)

    def _get_download_speed(self, data, delta):
        """Return the download speed in MB/s."""
        return round(
            (len(data) / self._min_bytes) / delta, 2
        )

    @pyqtSlot()
    def set_exit(self):
        """Time to shutdown the thread.

        Executed in the main thread."""
        self._exit_call = True

    def start(self, target):
        """Start the thread. Set the correct download options first."""
        self._target = target
        super().start()

    def _download_loop(self):
        """Read a chunck of the downloaded data at every iteration."""
        raw_data = bytes(0)
        sub_data = bytes(0)
        start = perf_counter()
        prev_downloaded = 0
        while True:
            try:
                data = self._data.read(self._CHUNK)
            except Exception:
                raise _SlowConnError
            else:
                delta = perf_counter() - start
                if not data:
                    break
                raw_data += data
                sub_data += data
                # Emit a progress signal only if at least self._min_bytes has been downloaded.
                if len(raw_data) - prev_downloaded >= self._min_bytes:
                    prev_downloaded = len(raw_data)
                    self.progress.emit(self._pretty_len(raw_data))
                if delta >= self._DELTAT:
                    self.speed_progress.emit(
                        self._get_download_speed(sub_data, delta)
                    )
                    sub_data = bytes(0)
                    start = perf_counter()
                if self._exit_call:
                    self._data.release_conn()
                    break
        return raw_data

    def run(self):
        """Override QThread.run. Download the database, images and audio samples.

        Handle all possible exceptions. Also extract the files
        in the destination folder."""
        self.status = ThreadStatus.UNDEFINED
        self._data = None

        try:
            self._data = get_pool_manager().request(
                'GET',
                self._target.url,
                preload_content=False,
            )
            raw_data = self._download_loop()
            if self._exit_call:
                self._exit_call = False
                return
        except Exception as e:  # No (or bad) internet connection.
            self._data.release_conn()
            if isinstance(e, _SlowConnError):
                self.status = ThreadStatus.SLOW_CONN_ERR
            else:
                self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        if self._data.status != 200:
            self.status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        if self._wrong_checksum(raw_data):
            return
        self._target.delete_files()
        self._extract(raw_data)

    def _wrong_checksum(self, raw_data):
        """Verify the checksum of the downloaded data and set the status accordingly."""
        try:
            is_checksum_ok = checksum_ok(raw_data, self._target.hash_code)
        except Exception:  # Invalid hash code.
            self.status = ThreadStatus.NO_CONNECTION_ERR
            return True
        else:
            if not is_checksum_ok:
                self.status = ThreadStatus.BAD_DOWNLOAD_ERR
                return True
            return False

    def _extract(self, raw_data):
        """Unzip and save the downloaded data into the destination folder."""
        try:
            self.progress.emit(Constants.EXTRACTING_CODE)
            self.speed_progress.emit(Constants.ZERO_FINAL_SPEED)
            with self._target.Extractor.open(fileobj=BytesIO(raw_data)) as zipped:
                zipped.extractall(path=self._target.dest_path)
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK


class UpdatesControllerThread(BaseDownloadThread):

    on_success = pyqtSignal(bool)

    def __init__(self, version_controller):
        super().__init__()
        self.version_controller = version_controller

    def run(self):
        if self.version_controller.update():
            self.on_success.emit(True)
        else:
            self.on_success.emit(False)


# class GenercWorkerThread(BaseDownloadThread):
#     def __init__(self, func, *args, **kwargs):
#         super().__init__()
#         self._args = args
#         self._kwargs = kwargs
#         self._func

#     def run(self):
#         self.status = ThreadStatus.UNDEFINED
#         try:
#             self._func(self._args, self._kwargs)
#         except Exception:
#             self.status = ThreadStatus.UNKNOWN_ERR
#         else:
#             self.status = ThreadStatus.OK


class _AsyncDownloader:
    """Mixin class for asynchronous threads."""

    async def _download_resource(self, session, link):
        """Return the content of 'link' as bytes."""
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=get_cacert_file()
        )
        resp = await session.get(link, ssl=ssl_context)
        return await resp.read()


class UpdateSpaceWeatherThread(BaseDownloadThread, _AsyncDownloader):
    """Subclass BaseDownloadThread. Download the space weather data."""

    _PROPERTIES = ("xray", "prot_el", "ak_index", "sgas", "geo_storm")

    def __init__(self, space_weather_data):
        """Initialize the a local space_weather_data."""
        super().__init__()
        self._space_weather_data = space_weather_data

    async def _download_property(self, session, property_name):
        """Download the data conteining the information of a specific property."""
        link = getattr(Constants, "SPACE_WEATHER_" + property_name.upper())
        data = await self._download_resource(session, link)
        setattr(self._space_weather_data, property_name, str(data, 'utf-8'))

    async def _download_image(self, session, n):
        """Download the data corresponding the n-th image displayed in the screen."""
        im = await self._download_resource(
            session, Constants.SPACE_WEATHER_IMGS[n]
        )
        self._space_weather_data.images[n].loadFromData(im)

    async def _download_resources(self):
        """Download all the data."""
        session = aiohttp.ClientSession()
        try:
            t = []
            for p in self._PROPERTIES:
                t.append(
                    asyncio.create_task(self._download_property(session, p))
                )

            tot_images = range(len(Constants.SPACE_WEATHER_IMGS))
            t1 = []
            for im_number in tot_images:
                t1.append(
                    asyncio.create_task(
                        self._download_image(session, im_number)
                    )
                )
            await asyncio.gather(*t, *t1)
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK
        finally:
            await session.close()

    def run(self):
        """Override QThread.run. Start the download of the data."""
        self.status = ThreadStatus.UNDEFINED
        asyncio.run(self._download_resources())


class UpdateForecastThread(BaseDownloadThread, _AsyncDownloader):
    """Subclass BaseDownloadThread. Download the forecast data."""

    class _PropertyName(Enum):
        """Enum used to differentiate between the two data needed."""
        FORECAST = auto()
        PROBABILITIES = auto()

    def __init__(self, owner):
        """Set the owner object (a ForecastData instance)."""
        super().__init__()
        self.owner = owner

    async def _download_property(self, session, link, prop_name):
        """Download the data from 'link' and set the corresponding property of the owner."""
        resp = await self._download_resource(session, link)
        resp = str(resp, 'utf-8')
        if prop_name is self._PropertyName.FORECAST:
            self.owner.forecast = resp
        if prop_name is self._PropertyName.PROBABILITIES:
            self.owner.probabilities = resp

    async def _download_resources(self):
        """Download all the data needed."""
        session = aiohttp.ClientSession()
        try:
            await asyncio.gather(
                asyncio.create_task(
                    self._download_property(
                        session,
                        Constants.SPACE_WEATHER_GEO_STORM,
                        self._PropertyName.FORECAST
                    )
                ),
                asyncio.create_task(
                    self._download_property(
                        session,
                        Constants.FORECAST_PROBABILITIES,
                        self._PropertyName.PROBABILITIES
                    )
                )
            )
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK
        finally:
            await session.close()

    def run(self):
        """Override QThread.run. Start the data download."""
        self.status = ThreadStatus.UNDEFINED
        asyncio.run(self._download_resources())
