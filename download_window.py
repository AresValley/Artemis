from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget
from threads import DownloadThread, ThreadStatus
from utilities import pop_up, resource_path
from constants import Constants, Messages

Ui_Download_window, _ = uic.loadUiType(
    resource_path("download_db_window.ui")
)


class DownloadWindow(QWidget, Ui_Download_window):
    """Subclass QWidget and Ui_Download_window. It is the window displayed during the database download."""

    complete = pyqtSignal()

    def __init__(self):
        """Initialize the window."""
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            # Qt.Window                |
            Qt.CustomizeWindowHint   |
            Qt.WindowTitleHint       |
            Qt.WindowCloseButtonHint  # |
            # Qt.WindowStaysOnTopHint
        )

        self._no_internet_msg = pop_up(self, title=Messages.NO_CONNECTION,
                                       text=Messages.NO_CONNECTION_MSG,
                                       connection=self.close)

        self._bad_db_download_msg = pop_up(self, title=Messages.BAD_DOWNLOAD,
                                           text=Messages.BAD_DOWNLOAD_MSG,
                                           connection=self.close)

        self._download_thread = DownloadThread()
        self._download_thread.finished.connect(self._wait_close)
        self._download_thread.progress.connect(self._display_progress)
        self.cancel_btn.clicked.connect(self._terminate_process)

    def start_download(self):
        """Start the download thread."""
        self._download_thread.start()

    def _downlaod_format_str(self, n, speed):
        """Return a well-formatted string with downloaded MB and speed."""
        return f"Downloaded MB: {n}\nSpeed: {speed} MB/s"

    def show(self):
        """Extends QWidget.show. Set downloaded MB and speed to zero."""
        self.status_lbl.setText(self._downlaod_format_str(0, 0))
        super().show()

    @pyqtSlot(int, float)
    def _display_progress(self, progress, speed):
        """Display the downloaded MB and speed."""
        if progress != Constants.EXTRACTING_CODE:
            self.status_lbl.setText(self._downlaod_format_str(progress, speed))
        elif progress == Constants.EXTRACTING_CODE:
            self.status_lbl.setText(Constants.EXTRACTING_MSG + '\n')

    @pyqtSlot()
    def _terminate_process(self):
        """Terminate the download thread and close."""
        if self._download_thread.isRunning():
            self._download_thread.terminate()
            self._download_thread.wait()
        self.close()

    @pyqtSlot()
    def _wait_close(self):
        """Decide the action based on the download thread status and close."""
        if self._download_thread.status is ThreadStatus.OK:
            self.complete.emit()
            self.close()
        elif self._download_thread.status is ThreadStatus.NO_CONNECTION_ERR:
            self._no_internet_msg.show()
        elif self._download_thread.status is ThreadStatus.BAD_DOWNLOAD_ERR:
            self._bad_db_download_msg.show()
        else:
            self.close()

    def reject(self):
        """Extends QWidget.reject. Terminate the download thread."""
        if self._download_thread.isRunning():
            self._download_thread.terminate()
            self._download_thread.wait()
        super().reject()
