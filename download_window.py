from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget
from threads import DownloadThread, ThreadStatus
from utilities import pop_up, resource_path
from constants import Constants, Messages

Ui_Download_window, _ = uic.loadUiType(resource_path("download_db_window.ui"))


class DownloadWindow(QWidget, Ui_Download_window):

    complete = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            #Qt.Window                |
            Qt.CustomizeWindowHint   |
            Qt.WindowTitleHint       |
            Qt.WindowCloseButtonHint #|
            # Qt.WindowStaysOnTopHint
        )

        self.no_internet_msg = pop_up(self, title=Messages.NO_CONNECTION,
                                      text=Messages.NO_CONNECTION_MSG,
                                      connection=self.close)

        self.bad_db_download_msg = pop_up(self, title=Messages.BAD_DOWNLOAD,
                                          text=Messages.BAD_DOWNLOAD_MSG,
                                          connection=self.close)

        self.download_thread = DownloadThread()
        self.download_thread.finished.connect(self.wait_close)
        self.download_thread.progress.connect(self.__display_progress)
        self.cancel_btn.clicked.connect(self.terminate_process)

    def __downlaod_format_str(self, n, speed):
        return f"Downloaded MB: {n}\nSpeed: {speed} MB/s"

    def show(self):
        self.status_lbl.setText(self.__downlaod_format_str(0, 0))
        super().show()

    @pyqtSlot(int, float)
    def __display_progress(self, progress, speed):
        if progress != Constants.EXTRACTING_CODE:
            self.status_lbl.setText(self.__downlaod_format_str(progress, speed))
        elif progress == Constants.EXTRACTING_CODE:
            self.status_lbl.setText(Constants.EXTRACTING_MSG + '\n')

    @pyqtSlot()
    def terminate_process(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        self.close()

    @pyqtSlot()
    def wait_close(self):
        if self.download_thread.status is ThreadStatus.OK:
            self.complete.emit()
            self.close()
        elif self.download_thread.status is ThreadStatus.NO_CONNECTION_ERR:
            self.no_internet_msg.show()
        elif self.download_thread.status is ThreadStatus.BAD_DOWNLOAD_ERR:
            self.bad_db_download_msg.show()
        else:
            self.close()

    def reject(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        super().reject()
