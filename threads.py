from enum import Enum, auto
from io import BytesIO
from os import mkdir
import os.path
from shutil import rmtree
import urllib3
from zipfile import ZipFile
from PyQt5.QtCore import QThread
import utilities

class ThreadStatus(Enum):
    ok = auto()
    no_connection_err = auto()
    no_file_err = auto()
    bad_download_err = auto()

class DownloadThread(QThread):
    def __init__(self, db_location, path):
        super().__init__()
        self.__db_location = db_location
        self.__path = path
        self.__status = None
        self.reason = 0

    @property
    def status(self):
        return self.__status

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            db = urllib3.PoolManager().request('GET', self.__db_location)
            # db = urllib.request.urlopen(self.__db_location)
            # raise urllib.error.URLError('Test')
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            # self.no_connection_error.emit()
            self.__status = ThreadStatus.no_connection_err
            return
        if db.status != 200:
            self.reason = db.reason
            # self.bad_download_error.emit()
            self.__status = ThreadStatus.bad_download_err
            return
        if not utilities.checksum_ok(db.data, "folder"):
            # self.bad_download_error.emit()
            self.__status = ThreadStatus.bad_download_err
            return
        if os.path.exists(self.__path):
            rmtree(self.__path)
        try:
            # data_folder = db.read()
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except:
            # self.bad_file_error.emit()
            self.__status = ThreadStatus.bad_file_err
            return
        else:
            self.__status = ThreadStatus.ok
