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
        self.manager = QNetworkAccessManager(self)
        self.reply = None

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.abortRequested.connect(self.on_abort)

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
        self._clear_ui()
        self.show_ui.emit()

        self.file_url = QUrl(url)
        self.file_size = None
        dest_path = QDir(save_path)
        self.dest_file = dest_path.filePath(self.file_url.fileName())
        self.file = QSaveFile(self.dest_file)

        if self.file.open(QIODevice.WriteOnly):
            # Start a GET HTTP request
            self.reply = self.manager.get(QNetworkRequest(self.file_url))
            self.reply.metaDataChanged.connect(self.on_metadata_changed)
            self.reply.downloadProgress.connect(self.on_progress)
            self.reply.finished.connect(self.on_finished)
            self.reply.readyRead.connect(self.on_ready_read)
            self.reply.errorOccurred.connect(self.on_error)
        else:
            self.close_ui.emit()
            self.show_popup_error(self.file.errorString())

    @Slot()
    def on_metadata_changed(self):
        """ Read the Content-Length header once the reply's metadata
            becomes available. If the header is missing, leave
            file_size as None and set the progress bar to
            'indeterminate' mode instead.
        """
        if not self.reply:
            return

        content_length = self.reply.header(QNetworkRequest.ContentLengthHeader)
        if content_length is not None:
            self.file_size = int(content_length)
        else:
            self.set_indeterminate_bar.emit()

    @Slot()
    def on_abort(self):
        """ Stop the download when user presses the abort button
        """
        if self.reply:
            self.reply.abort()


    @Slot()
    def on_ready_read(self):
        """ Write available bytes to the file
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                self.file.write(self.reply.readAll())


    @Slot()
    def on_finished(self):
        """ Finalize the download process and, if no errors
            occurs, emits the finished signal usefull for
            a callback
        """
        if not self.reply:
            return

        has_error = self.reply.error() != QNetworkReply.NoError

        if self.file:
            if not has_error:
                self.file.commit()
            else:
                self.file.cancelWriting()

        self.reply.deleteLater()
        self.reply = None
        
        if not has_error:
            self.finished.emit()

        self.close_ui.emit()


    @Slot(int, int)
    def on_progress(self, bytesReceived: int, bytesTotal: int):
        """ Update progress bar and status label

            Note: file_size (from the Content-Length header) may not be
            populated yet on the very first call, since metaDataChanged
            and the first downloadProgress signal can race. In that case
            we fall back to bytesTotal for this tick only; file_size
            takes over on subsequent calls once available.
        """
        total = self.file_size if self.file_size is not None else bytesTotal

        if total > 0:
            self.update_status.emit(f"{bytesReceived/10**6:.1f} Mb / {total/10**6:.1f} Mb")
            self.update_progress_bar.emit(bytesReceived, total)
        else:
            self.update_status.emit(f"{bytesReceived/10**6:.1f} Mb")


    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError):
        """ Show a message if an error happen during download
        """
        if code == QNetworkReply.OperationCanceledError:
            return

        if self.reply:
            self.close_ui.emit()
            self.show_popup_error(
                self.reply.errorString()
            )

    def _clear_ui(self):
        self.update_progress_bar.emit(0, 0)
        self.update_status.emit('')


    def show_popup_error(self, error_msg):
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_ERROR,
            Messages.GENERIC_ERROR,
            Messages.GENERIC_ERROR_MSG.format(error_msg)
        )
