from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from threads import UpadteSpaceWeatherThread, ThreadStatus


class SpaceWeatherData(QObject):
    update_complete = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''
        self.images = [
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap()
        ]
        self.__update_thread = UpadteSpaceWeatherThread(self)
        self.__update_thread.finished.connect(self.__parse_and_emit_signal)

    @property
    def is_updating(self):
        return self.__update_thread.isRunning()

    @pyqtSlot()
    def update(self):
        self.__update_thread.start()

    def __parse_data(self):
        double_split = lambda string: [i.split() for i in string.splitlines()]
        self.xray      = double_split(self.xray)
        self.prot_el   = double_split(self.prot_el)
        self.ak_index  = double_split(self.ak_index)
        self.sgas      = double_split(self.sgas)
        self.geo_storm = double_split(self.geo_storm)

    def remove_data(self):
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''
        self.images = [
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap()
        ]

    @pyqtSlot()
    def __parse_and_emit_signal(self):
        status_ok = False
        if self.__update_thread.status is ThreadStatus.OK:
            status_ok = True
            self.__parse_data()
        self.update_complete.emit(status_ok)

    def shutdown_thread(self):
        self.__update_thread.terminate()
        self.__update_thread.wait()
