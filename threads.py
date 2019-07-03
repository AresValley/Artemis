import asyncio
from enum import Enum, auto
from io import BytesIO
from math import ceil
import os.path
from shutil import rmtree
from time import perf_counter
from zipfile import ZipFile
import aiohttp
import urllib3
from PyQt5.QtCore import QThread, pyqtSignal
from constants import Constants, Database, ChecksumWhat
from utilities import checksum_ok

import encodings.idna

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

    def __del__(self):
        """Force the termination of the thread."""
        self.terminate()
        self.wait()


class DownloadThread(BaseDownloadThread):
    """Subclass BaseDownloadThread. Download the database, images and audio samples."""

    progress = pyqtSignal(int)
    speed_progress = pyqtSignal(float)
    _CHUNK = 128 * 1024
    _MEGA = 1024**2
    _DELTAT = 2

    def __init__(self):
        """Just call super().__init__."""
        self._db = None
        self._exit_call = False
        super().__init__()

    def _pretty_len(self, byte_obj):
        """Return a well-formatted number of downloaded MB."""
        mega = len(byte_obj) / self._MEGA
        if mega.is_integer():
            return int(mega)
        else:
            return ceil(mega)

    def _get_download_speed(self, data, delta):
        """Return the download speed in MB/s."""
        return round(
            (len(data) / self._MEGA) / delta, 2
        )

    def set_exit(self):
        self._exit_call = True

    def run(self):
        """Override QThread.run. Download the database, images and audio samples.

        Handle all possible exceptions. Also extract the files
        in the local folder."""
        self.status = ThreadStatus.UNDEFINED
        self._db = None
        raw_data = bytes(0)
        sub_data = bytes(0)
        try:
            self._db = urllib3.PoolManager().request(
                'GET',
                Database.LINK_LOC,
                preload_content=False,
                timeout=4.0
            )
            start = perf_counter()
            prev_downloaded = 0
            while True:
                try:
                    data = self._db.read(self._CHUNK)
                except Exception:
                    raise _SlowConnError
                else:
                    delta = perf_counter() - start
                    if not data:
                        break
                    raw_data += data
                    sub_data += data
                    # Emit a progress signal only if at least 1 MB has been downloaded.
                    if len(raw_data) - prev_downloaded >= self._MEGA:
                        prev_downloaded = len(raw_data)
                        self.progress.emit(self._pretty_len(raw_data))
                    if delta >= self._DELTAT:
                        self.speed_progress.emit(
                            self._get_download_speed(sub_data, delta)
                        )
                        sub_data = bytes(0)
                        start = perf_counter()
                    if self._exit_call:
                        self._exit_call = False
                        self._db.release_conn()
                        return
        except Exception as e:  # No (or bad) internet connection.
            self._db.release_conn()
            if isinstance(e, _SlowConnError):
                self.status = ThreadStatus.SLOW_CONN_ERR
            else:
                self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        if self._db.status != 200:
            self.status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        try:
            is_checksum_ok = checksum_ok(raw_data, ChecksumWhat.FOLDER)
        except Exception:  # checksum_ok unable to connect to the reference.
            self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        else:
            if not is_checksum_ok:
                self.status = ThreadStatus.BAD_DOWNLOAD_ERR
                return
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER)
        try:
            self.progress.emit(Constants.EXTRACTING_CODE)
            self.speed_progress.emit(Constants.ZERO_FINAL_SPEED)
            with ZipFile(BytesIO(raw_data)) as zipped:
                zipped.extractall()
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK


class _AsyncDownloader:
    """Mixin class for asynchronous threads."""

    async def _download_resource(self, session, link):
        """Return the content of 'link' as bytes."""
        resp = await session.get(link)
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
