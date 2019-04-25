from enum import Enum, auto
from io import BytesIO
from os import mkdir
import os.path
from shutil import rmtree
import urllib3
from zipfile import ZipFile
from PyQt5.QtCore import QThread
from constants import Constants, Database, ChecksumWhat
from utilities import checksum_ok

class ThreadStatus(Enum):
    OK                = auto()
    NO_CONNECTION_ERR = auto()
    UNKNOWN_ERR       = auto()
    BAD_DOWNLOAD_ERR  = auto()
    UNDEFINED         = auto()

class DownloadThread(QThread):
    def __init__(self):
        super().__init__()
        self.__status = ThreadStatus.UNDEFINED
        self.reason = 0

    @property
    def status(self):
        return self.__status

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            db = urllib3.PoolManager().request('GET', Database.LINK_LOC)
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            self.__status = ThreadStatus.NO_CONNECTION_ERR
            return
        if db.status != 200:
            self.reason = db.reason
            self.__status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        try:
            is_checksum_ok = checksum_ok(db.data, ChecksumWhat.FOLDER)
        except:
            self.__status = ThreadStatus.NO_CONNECTION_ERR
            return
        else:
            if not is_checksum_ok:
                self.__status = ThreadStatus.BAD_DOWNLOAD_ERR
                return
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER)
        try:
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except:
            self.__status = ThreadStatus.UNKNOWN_ERR
        else:
            self.__status = ThreadStatus.OK


class UpadteSpaceWeatherThread(QThread):
    def __init__(self, space_weather_data):
        super().__init__()
        self.__status = ThreadStatus.UNDEFINED
        self.__space_weather_data = space_weather_data

    @property
    def status(self):
        return self.__status

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            self.__space_weather_data.xray = str(urllib3.PoolManager().request('GET', Constants.FORECAST_XRAY).data, 'utf-8')
            self.__space_weather_data.prot_el = str(urllib3.PoolManager().request('GET', Constants.FORECAST_PROT).data, 'utf-8')
            self.__space_weather_data.ak_index = str(urllib3.PoolManager().request('GET', Constants.FORECAST_AK_IND).data, 'utf-8')
            self.__space_weather_data.sgas = str(urllib3.PoolManager().request('GET', Constants.FORECAST_SGAS).data, 'utf-8')
            self.__space_weather_data.geo_storm = str(urllib3.PoolManager().request('GET', Constants.FORECAST_G).data, 'utf-8')
            self.__space_weather_data.images[0].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_0).data)
            self.__space_weather_data.images[1].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_1).data)
            self.__space_weather_data.images[2].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_2).data)
            self.__space_weather_data.images[3].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_3).data)
            self.__space_weather_data.images[4].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_4).data)
            self.__space_weather_data.images[5].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_5).data)
            self.__space_weather_data.images[6].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_6).data)
            self.__space_weather_data.images[7].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_7).data)
            self.__space_weather_data.images[8].loadFromData(urllib3.PoolManager().request('GET', Constants.FORECAST_IMG_8).data)
        except:
            self.__status = ThreadStatus.UNKNOWN_ERR
        else:
            self.__status = ThreadStatus.OK
