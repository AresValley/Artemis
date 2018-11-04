from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from threads import DownloadThread, ThreadStatus
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
        self.no_internet_msg = QMessageBox(self)
        self.no_internet_msg.setWindowTitle("No internet connection")
        self.no_internet_msg.setText("Unable to establish an internet connection.")
        # self.no_internet_msg.buttonClicked.connect(self.close)
        self.no_internet_msg.finished.connect(self.close)

        self.bad_db_download_msg = QMessageBox(self)
        self.bad_db_download_msg.setWindowTitle("Something wrong")
        self.bad_db_download_msg.setText("""Something went wrong with the downaload.
        Check your internet connection and try again.""")
        self.bad_db_download_msg.finished.connect(self.close)

        self.bad_file_msg = QMessageBox(self)
        self.bad_file_msg.setWindowTitle("Bad file detected")
        self.bad_file_msg.setText("""The downloaded file seems to be corrupted.
        The old database has not been deleted and
        the downloaded file has been discarded.""")
        self.bad_file_msg.finished.connect(self.close)

        self.download_thread = DownloadThread()
        self.download_thread.finished.connect(self.wait_close)

        self.cancel_btn.clicked.connect(self.terminate_process)

    def show_no_connection_warning(self):
        self.bad_db_download_msg.setText(f"""Unable to correctly download the database.
        Reason: {self.download_thread.reason}""")
        self.no_internet_msg.show()
        self.everything_ok = False

    def show_bad_download_warning(self):
        self.bad_db_download_msg.show()
        self.everything_ok = False

    @pyqtSlot()
    def terminate_process(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()    
        self.close()

    @pyqtSlot()
    def wait_close(self):
        if self.download_thread.status == ThreadStatus.ok:
            self.close()
        elif self.download_thread.status == ThreadStatus.no_connection_err:
            self.show_no_connection_warning()
        elif self.download_thread.status == ThreadStatus.bad_download_err:
            self.show_bad_download_warning
        else:
            self.close()

    def reject(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        super().reject()
