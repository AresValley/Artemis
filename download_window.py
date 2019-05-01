from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget
from threads import DownloadThread, ThreadStatus
from utilities import pop_up, resource_path
from constants import Messages

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
        self.cancel_btn.clicked.connect(self.terminate_process)

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
