from io import BytesIO
from os import mkdir
import os.path
from shutil import rmtree
import urllib3
from zipfile import ZipFile
from PyQt5.QtCore import QThread, pyqtSignal
import utilities

class DownloadThread(QThread):
    no_connection_error = pyqtSignal()
    bad_db_download_error = pyqtSignal()
    bad_file_error = pyqtSignal()

    def __init__(self, db_location, path):
        super().__init__()
        self.__db_location = db_location
        self.__path = path
        self.regular_execution = True
        self.reason = 0

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        try:
            db = urllib3.PoolManager().request('GET', self.__db_location)
            # db = urllib.request.urlopen(self.__db_location)
            # raise urllib.error.URLError('Test')
        except urllib3.exceptions.MaxRetryError: # No internet connection.
            self.regular_execution = False
            self.no_connection_error.emit()
            return
        if db.status != 200:
            self.regular_execution = False
            self.reason = db.reason
            self.bad_db_download_error.emit()
            return
        if not utilities.checksum_ok(db.data, "folder"):
            regular_execution = False
            self.bad_db_download_error.emit()
            return
        if os.path.exists(self.__path):
            rmtree(self.__path)
        try:
        # data_folder = db.read()
            # data_folder = db.data
            with ZipFile(BytesIO(db.data)) as zipped:
                zipped.extractall()
        except:
            self.regular_execution = False
            self.bad_file_error.emit()
            return
