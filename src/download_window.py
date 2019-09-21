from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget
from threads import DownloadThread, ThreadStatus
from utilities import pop_up
from executable_utilities import resource_path
from constants import Constants, Messages


Ui_Download_window, _ = uic.loadUiType(
    resource_path("download_db_window.ui")
)


class DownloadWindow(QWidget, Ui_Download_window):
    """Subclass QWidget and Ui_Download_window. It is the window displayed during
    downloads and software updates."""

    complete = pyqtSignal()
    closed = pyqtSignal()
    _PROGRESS_CONEVERSION_FACTOR = 1024

    def __init__(self):
        """Initialize the window."""
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            # Qt.Window                |
            Qt.CustomizeWindowHint   |
            Qt.WindowTitleHint       |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )

        self._no_internet_msg = pop_up(self, title=Messages.NO_CONNECTION,
                                       text=Messages.NO_CONNECTION_MSG,
                                       connection=self.close)

        self._bad_db_download_msg = pop_up(self, title=Messages.BAD_DOWNLOAD,
                                           text=Messages.BAD_DOWNLOAD_MSG,
                                           connection=self.close)

        self._slow_conn_msg = pop_up(self, title=Messages.SLOW_CONN,
                                     text=Messages.SLOW_CONN_MSG,
                                     connection=self.close)

        self._download_thread = DownloadThread()
        self._download_thread.finished.connect(self._wait_close)
        self._download_thread.progress.connect(self._display_progress)
        self._download_thread.speed_progress.connect(self._display_speed)
        self.closed.connect(self._download_thread.set_exit)
        self.cancel_btn.clicked.connect(self._terminate_process)
        self._size = 0
        self.target = None

    def _prepare_progress_bar(self, size):
        """Prepare the progress bar for the upcoming download."""
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(size)
        self._progress_bar.setValue(0)

    def activate(self, target):
        """Start the download thread."""
        self._size = target.size
        self.target = target.target
        self._prepare_progress_bar(target.size)
        self._download_thread.start(target)
        self.show()

    def _download_format_str(self, n):
        """Return a well-formatted string with the downloaded MB."""
        return f"Downloaded: {n} MB"

    @pyqtSlot(float)
    def _display_speed(self, speed):
        """Display the download speed."""
        ret = "Speed: "
        if speed == Constants.ZERO_INITIAL_SPEED:
            ret += "Calculating..."
        elif speed == 0.0:
            ret += "VERY SLOW"
        elif speed == Constants.ZERO_FINAL_SPEED:
            ret = ""
        else:
            ret += f"{speed} MB/s"
        self.speed_lbl.setText(ret)

    @pyqtSlot(int)
    def _display_progress(self, progress):
        """Display the downloaded MB."""
        if progress != Constants.EXTRACTING_CODE:
            self.status_lbl.setText(self._download_format_str(progress))
        elif progress == Constants.EXTRACTING_CODE:
            self.status_lbl.setText(Constants.EXTRACTING_MSG)
        if self._size > 0:
            self._progress_bar.setValue(progress * self._PROGRESS_CONEVERSION_FACTOR)

    def show(self):
        """Extends QWidget.show. Set downloaded MB and speed to zero."""
        self._display_progress(0)
        self._display_speed(Constants.ZERO_INITIAL_SPEED)
        super().show()

    def _stop_thread(self):
        """Ask the download thread to stop."""
        if self._download_thread.isRunning():
            self.closed.emit()
            self._download_thread.wait()

    @pyqtSlot()
    def _terminate_process(self):
        """Terminate the download thread and close."""
        self._stop_thread()
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
        elif self._download_thread.status is ThreadStatus.SLOW_CONN_ERR:
            self._slow_conn_msg.show()
        else:
            self.close()

    def reject(self):
        """Extends QWidget.reject. Terminate the download thread."""
        self._stop_thread()
        super().reject()
