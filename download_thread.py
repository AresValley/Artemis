from io import BytesIO
from os import mkdir
import os.path
from shutil import rmtree
import urllib
from zipfile import ZipFile
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    no_connection_error = pyqtSignal()
    bad_db_download_error = pyqtSignal()

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
        if os.path.exists(self.__path):
            rmtree(self.__path)
        try:
            db = urllib.request.urlopen(self.__db_location)
            # raise urllib.error.URLError('Test')
        except urllib.error.URLError: # No internet connection.
            self.regular_execution = False
            self.no_connection_error.emit()
            return
        if db.status != 200:
            self.regular_execution = False
            self.reason = db.reason
            self.bad_db_download_error.emit()
            return
        try:
            with ZipFile(BytesIO(db.read())) as zipped:
                zipped.extractall()
        except:
            pass
