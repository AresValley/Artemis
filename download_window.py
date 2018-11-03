from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from download_thread import DownloadThread
Ui_Download_window, _ = uic.loadUiType("download_db_window.ui")

class DownloadWindow(QWidget, Ui_Download_window):
    def __init__(self, db_location, data_folder):
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
        self.no_internet_msg.setText("Unable to establish an internet connection")
        # self.no_internet_msg.buttonClicked.connect(self.close)
        self.no_internet_msg.finished.connect(self.close)

        self.bad_db_download_msg = QMessageBox(self)
        self.bad_db_download_msg.setWindowTitle("Something wrong")
        self.bad_db_download_msg.finished.connect(self.close)

        self.download_thread = DownloadThread(db_location, data_folder)
        self.download_thread.finished.connect(self.wait_close)
        self.download_thread.no_connection_error.connect(self.show_no_connection_warning)
        self.download_thread.bad_db_download_error.connect(self.show_bad_download_warning)

        self.cancel_btn.clicked.connect(self.terminate_process)

    @pyqtSlot()
    def show_no_connection_warning(self):
        self.bad_db_download_msg.setText(f"Unable to correctly download the database.\nReason: {self.download_thread.reason}")
        self.no_internet_msg.show()
        self.everything_ok = False

    @pyqtSlot()
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
        if self.download_thread.regular_execution:
            self.close() 

    def reject(self):
        if self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        super().reject()
