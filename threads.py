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
    ok = auto()
    no_connection_err = auto()
    no_file_err = auto()
    bad_download_err = auto()

class DownloadThread(QThread):
    def __init__(self):
        super().__init__()
        self.__status = ThreadStatus.ok
        self.reason = 0

    @property
    def status(self):
        return self.__status

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            db = urllib3.PoolManager().request('GET', Constants.db_location)
            # db = urllib.request.urlopen(Constants.db_location)
            # raise urllib.error.URLError('Test')
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            self.__status = ThreadStatus.no_connection_err
            return
        if db.status != 200:
            self.reason = db.reason
            self.__status = ThreadStatus.bad_download_err
            return
        if not checksum_ok(db.data, "folder"):
            self.__status = ThreadStatus.bad_download_err
            return
        if os.path.exists(Constants.data_folder):
            rmtree(Constants.data_folder)
        try:
            # data_folder = db.read()
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except:
            self.__status = ThreadStatus.bad_file_err
