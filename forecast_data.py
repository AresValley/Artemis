from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

from threads import UpadteForecastThread, ThreadStatus
from utilities import double_split

class ForecastData(QObject):
    update_complete = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''
        self.__update_thread = UpadteForecastThread(self)
        self.__update_thread.finished.connect(self.__parse_and_emit_signal)

    @pyqtSlot()
    def update(self):
        self.__update_thread.start()

    def __parse_data(self):
        self.xray = double_split(str(self.xray))
        self.prot_el = double_split(str(self.prot_el))
        self.ak_index = double_split(str(self.ak_index))
        self.sgas = double_split(str(self.sgas))
        self.geo_storm = double_split(str(self.geo_storm))

    def remove_data(self):
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''

    @pyqtSlot()
    def __parse_and_emit_signal(self):
        if self.__update_thread.status != ThreadStatus.OK:
            status_ok = False
        else:
            status_ok = True
            self.__parse_data()
        self.update_complete.emit(status_ok)
