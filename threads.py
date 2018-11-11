from enum import Enum, auto
from io import BytesIO
from os import mkdir
import os.path
from shutil import rmtree
import urllib3
from zipfile import ZipFile
from PyQt5.QtCore import QThread
from utilities import checksum_ok, Constants

class ThreadStatus(Enum):
    OK = auto()
    NO_CONNECTION_ERR = auto()
    UNKNOWN_ERR = auto()
    BAD_DOWNLOAD_ERR = auto()

class DownloadThread(QThread):
    def __init__(self):
        super().__init__()
        self.__status = ThreadStatus.OK
        self.reason = 0

    @property
    def status(self):
        return self.__status

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            db = urllib3.PoolManager().request('GET', Constants.DB_LOCATION)
            # db = urllib.request.urlopen(Constants.DB_LOCATION)
            # raise urllib.error.URLError('Test')
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            self.__status = ThreadStatus.NO_CONNECTION_ERR
            return
        if db.status != 200:
            self.reason = db.reason
            self.__status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        if not checksum_ok(db.data, "folder"):
            self.__status = ThreadStatus.BAD_DOWNLOAD_ERR
            return
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER)
        try:
            # data_folder = db.read()
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except:
            self.__status = ThreadStatus.UNKNOWN_ERR
