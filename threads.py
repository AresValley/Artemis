import asyncio
from enum import Enum, auto
from io import BytesIO
import os.path
from shutil import rmtree
from zipfile import ZipFile
import aiohttp
import urllib3
from PyQt5.QtCore import QThread
from constants import Constants, Database, ChecksumWhat
from utilities import checksum_ok


class ThreadStatus(Enum):
    OK                = auto()
    NO_CONNECTION_ERR = auto()
    UNKNOWN_ERR       = auto()
    BAD_DOWNLOAD_ERR  = auto()
    UNDEFINED         = auto()


class _BaseDownloadThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = ThreadStatus.UNDEFINED

    def __del__(self):
        self.terminate()
        self.wait()
        super().__del__()


class DownloadThread(_BaseDownloadThread):
    def __init__(self):
        super().__init__()
        self.reason = 0

    def run(self):
        self.status = ThreadStatus.UNDEFINED
        try:
            db = urllib3.PoolManager().request('GET', Database.LINK_LOC)
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            self.status = ThreadStatus.NO_CONNECTION_ERR
            return
        if db.status != 200:
            self.reason = db.reason
            self.status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        try:
            is_checksum_ok = checksum_ok(db.data, ChecksumWhat.FOLDER)
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
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK


class UpadteSpaceWeatherThread(_BaseDownloadThread):

    __properties = ("xray", "prot_el", "ak_index", "sgas", "geo_storm")

    def __init__(self, space_weather_data):
        super().__init__()
        self.__space_weather_data = space_weather_data

    async def __download_resource(self, session, link):
        resp = await session.get(link)
        return await resp.read()

    async def __download_property(self, session, property_name):
        link = getattr(Constants, "FORECAST_" + property_name.upper())
        data = await self.__download_resource(session, link)
        setattr(self.__space_weather_data, property_name, str(data, 'utf-8'))

    async def __download_image(self, session, n):
        im = await self.__download_resource(session, Constants.FORECAST_IMGS[n])
        self.__space_weather_data.images[n].loadFromData(im)

    async def __download_resources(self, *links):
        session = aiohttp.ClientSession()
        try:
            t = []
            for p in self.__properties:
                t.append(
                    asyncio.create_task(self.__download_property(session, p))
                )

            tot_images = range(len(Constants.FORECAST_IMGS))
            t1 = []
            for im_number in tot_images:
                t1.append(
                    asyncio.create_task(self.__download_image(session, im_number))
                )
            await asyncio.gather(*t, *t1)
        except Exception:
            self.status = ThreadStatus.UNKNOWN_ERR
        else:
            self.status = ThreadStatus.OK
        finally:
            await session.close()

    def run(self):
        self.status = ThreadStatus.UNDEFINED
        asyncio.run(self.__download_resources())
