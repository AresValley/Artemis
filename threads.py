import asyncio
from enum import Enum, auto
from io import BytesIO
from math import ceil
import os.path
from shutil import rmtree
from time import time
from zipfile import ZipFile
import aiohttp
import urllib3
from PyQt5.QtCore import QThread, pyqtSignal
from constants import Constants, Database, ChecksumWhat
from utilities import checksum_ok


class ThreadStatus(Enum):
    """Possible thread status."""

    OK                = auto()
    NO_CONNECTION_ERR = auto()
    UNKNOWN_ERR       = auto()
    BAD_DOWNLOAD_ERR  = auto()
    UNDEFINED         = auto()


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

    progress = pyqtSignal(int, float)
    CHUNK = 1024**2

    def __init__(self):
        """Just call super().__init__."""
        super().__init__()

    def _pretty_len(self, byte_obj):
        """Return a well-formatted number of downloaded MB."""
        mega = len(byte_obj) / self.CHUNK
        if mega.is_integer():
            return int(mega)
        else:
            return ceil(mega)

    def _get_download_speed(self, data, delta):
        """Return the download speed in MB/s."""
        return round(
            (len(data) / self.CHUNK) / delta, 2
        )

    def run(self):
        """Override QThread.run. Download the database, images and audio samples.

        Handle all possible exceptions. Also extract the files
        in the local folder."""
        self.status = ThreadStatus.UNDEFINED
        raw_data = bytes(0)
        try:
            db = urllib3.PoolManager().request(
                'GET',
                Database.LINK_LOC,
                preload_content=False
            )
            while True:
                start = time()
                data = db.read(self.CHUNK)
                delta = time() - start
                if not data:
                    break
                raw_data += data
                self.progress.emit(
                    self._pretty_len(raw_data),
                    self._get_download_speed(data, delta)
                )
            db.release_conn()
        except Exception: # No internet connection.
            db.release_conn()
            self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        if db.status != 200:
            self.status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        try:
            is_checksum_ok = checksum_ok(raw_data, ChecksumWhat.FOLDER)
        except Exception:
            self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        else:
            if not is_checksum_ok:
                self.status = ThreadStatus.BAD_DOWNLOAD_ERR
                return
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER)
        try:
            self.progress.emit(Constants.EXTRACTING_CODE, 0.0)
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
    """Subclass BaseDownloadThread. Downlaod the space weather data."""

    _properties = ("xray", "prot_el", "ak_index", "sgas", "geo_storm")

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
            for p in self._properties:
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
