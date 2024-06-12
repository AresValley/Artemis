import requests

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QUrl, QSaveFile, QDir, QIODevice
from PySide6.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager

from artemis.utils.constants import Messages


class UIDownloader(QObject):
    # Python > QML Signals
    show_ui = Signal()
    close_ui = Signal()
    update_progress_bar = Signal(int, int)
    set_indeterminate_bar = Signal()
    update_status = Signal(str)
    finished = Signal()


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Downloader.qml')
        self._window = self._engine.rootObjects()[0]

        self.file_url = None
        self.file_size = None
        self.dest_file = None
        self.file = None
        self.manager = None
        self.reply = None

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.onAbort.connect(self.on_abort)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.close_ui.connect(self._window.close)
        self.update_progress_bar.connect(self._window.updateProgressBar)
        self.set_indeterminate_bar.connect(self._window.setIndeterminateBar)
        self.update_status.connect(self._window.updateStatus)


    def on_start(self, url, save_path):
        """ Start the download process using the specified URL

        Args:
            url (str): url from where download the file
            save_path (str): path where to save the downloaded file
        """

        self.show_ui.emit()

        self.file_url = QUrl(url)
        self.file_size = self._get_filesize(url)
        dest_path = QDir(save_path)
        self.dest_file = dest_path.filePath(self.file_url.fileName())
        self.file = QSaveFile(self.dest_file)

        if self.file.open(QIODevice.WriteOnly):
            # Start a GET HTTP request
            self.manager = QNetworkAccessManager(self)
            self.reply = self.manager.get(QNetworkRequest(self.file_url))
            self.reply.downloadProgress.connect(self.on_progress)
            self.reply.finished.connect(self.on_finished)
            self.reply.readyRead.connect(self.on_ready_read)
            self.reply.errorOccurred.connect(self.on_error)
        else:
            self.close_ui.emit()
            self.show_popup_error(
                self.file.errorString()
            )


    @Slot()
    def on_abort(self):
        """ Stop the download when user presses the abort button
        """
        if self.reply:
            self.reply.abort()
            self.update_progress_bar.emit(0, 0)

        if self.file:
            self.file.cancelWriting()


    @Slot()
    def on_ready_read(self):
        """ Write available bytes to the file
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                self.file.write(self.reply.readAll())


    @Slot()
    def on_finished(self):
        """ Finalize the download process and if no errors
            occurrs emits the finished signal usefulle for
            a callback
        """
        if self.reply:
            self.reply.deleteLater()

        if self.file:
            self.file.commit()
        
        if self.reply.error() == QNetworkReply.NoError:
            self.finished.emit()

        self.close_ui.emit()


    @Slot(int, int)
    def on_progress(self, bytesReceived: int):
        """ Update progress bar and status label
        """
        if self.file_size is not None:
            self.update_status.emit("{:.1f} Mb / {:.1f} Mb".format(bytesReceived/10**6, self.file_size/10**6))
            self.update_progress_bar.emit(bytesReceived, self.file_size)
        else:
            self.update_status.emit("{:.1f} Mb".format(bytesReceived/10**6))


    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError):
        """ Show a message if an error happen during download
        """
        if self.reply:
            self.close_ui.emit()
            self.show_popup_error(
                self.reply.errorString()
            )


    def _get_filesize(self, url):
        """ Get the file size by sending a HEAD request to the URL.
            If the Content-Length in HTTP headers is missing, returns None

        Args:
            url (str): URL to check the file size
        """
        try:
            response = requests.get(url, stream=True)
            size = int(response.headers.get('content-length'))
            return size
        except:
            self.set_indeterminate_bar.emit()
            return None


    def show_popup_error(self, error_msg):
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_ERROR,
            Messages.GENERIC_ERROR,
            Messages.GENERIC_ERROR_MSG.format(error_msg)
        )
