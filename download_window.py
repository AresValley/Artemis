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

        self.__no_internet_msg = pop_up(self, title=Messages.NO_CONNECTION,
                                        text=Messages.NO_CONNECTION_MSG,
                                        connection=self.close)

        self.__bad_db_download_msg = pop_up(self, title=Messages.BAD_DOWNLOAD,
                                            text=Messages.BAD_DOWNLOAD_MSG,
                                            connection=self.close)

        self.__download_thread = DownloadThread()
        self.__download_thread.finished.connect(self.__wait_close)
        self.__download_thread.progress.connect(self.__display_progress)
        self.cancel_btn.clicked.connect(self.__terminate_process)

    def start_download(self):
        self.__download_thread.start()

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
    def __terminate_process(self):
        if self.__download_thread.isRunning():
            self.__download_thread.terminate()
            self.__download_thread.wait()
        self.close()

    @pyqtSlot()
    def __wait_close(self):
        if self.__download_thread.status is ThreadStatus.OK:
            self.complete.emit()
            self.close()
        elif self.__download_thread.status is ThreadStatus.NO_CONNECTION_ERR:
            self.__no_internet_msg.show()
        elif self.__download_thread.status is ThreadStatus.BAD_DOWNLOAD_ERR:
            self.__bad_db_download_msg.show()
        else:
            self.close()

    def reject(self):
        if self.__download_thread.isRunning():
            self.__download_thread.terminate()
            self.__download_thread.wait()
        super().reject()
