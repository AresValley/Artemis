from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget
from threads import DownloadThread, ThreadStatus
from utilities import throwable_message
from constants import Messages

Ui_Download_window, _ = uic.loadUiType("download_db_window.ui")

class DownloadWindow(QWidget, Ui_Download_window):
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
        self.everything_ok = True

        self.no_internet_msg = throwable_message(self, title = Messages.NO_CONNECTION, 
                                                 text = Messages.NO_CONNECTION_MSG, 
                                                 connection = self.close)

        self.bad_db_download_msg = throwable_message(self, title = Messages.BAD_DOWNLOAD,
                                                     text = Messages.BAD_DOWNLOAD_MSG,
                                                     connection = self.close)

        # Never used (should exploit the checksum check for the single file)
        self.bad_file_msg = throwable_message(self, title = Messages.BAD_FILE,
                                              text = Messages.BAD_FILE_MSG,
                                              connection = self.close)

        self.download_thread = DownloadThread()
        self.download_thread.finished.connect(self.wait_close)

        self.cancel_btn.clicked.connect(self.terminate_process)

    def show_no_connection_warning(self):
        self.no_internet_msg.show()
        self.everything_ok = False

    def show_bad_download_warning(self):
        self.bad_db_download_msg.show()
        self.everything_ok = False

    def show_bad_file_warning(self):
        self.bad_file_msg.show()
        self.everything_ok = False

    @pyqtSlot()
    def terminate_process(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()    
        self.close()

    @pyqtSlot()
    def wait_close(self):
        if self.download_thread.status == ThreadStatus.OK:
            self.close()
        elif self.download_thread.status == ThreadStatus.NO_CONNECTION_ERR:
            self.show_no_connection_warning()
        elif self.download_thread.status == ThreadStatus.BAD_DOWNLOAD_ERR:
            self.show_bad_download_warning()
        else:
            self.close()

    def reject(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        super().reject()
