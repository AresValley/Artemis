from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QUrl, QSaveFile, QDir, QIODevice
from PySide6.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager

from artemis.utils.config_utils import *
from artemis.utils.sys_utils import delete_file, delete_dir, match_hash, unpack_tar
from artemis.utils.constants import Messages
from artemis.utils.path_utils import DATA_DIR


class UIDownloader(QObject):
    # Python > QML Signals
    show_ui = Signal()
    close_ui = Signal()
    update_progress_bar = Signal(int, int)
    update_status = Signal(str)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Downloader.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.onAbort.connect(self.on_abort)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.close_ui.connect(self._window.close)
        self.update_progress_bar.connect(self._window.updateProgressBar)
        self.update_status.connect(self._window.updateStatus)


    @Slot()
    def on_start(self):
        """ Start the download of the DB taking the needed url and size from
            the attributes of the UpdatesController class
        """
        url_file = QUrl(self._parent.network_manager.remote_db_url)
        dest_path = QDir(DATA_DIR)
        self.dest_file = dest_path.filePath(url_file.fileName())
        self.file = QSaveFile(self.dest_file)

        if self.file.open(QIODevice.WriteOnly):
            # Start a GET HTTP request
            self.manager = QNetworkAccessManager(self)
            self.reply = self.manager.get(QNetworkRequest(url_file))
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
        """ Stop the download when user press abort button """
        if self.reply:
            self.reply.abort()
            self.update_progress_bar.emit(0, 0)

        if self.file:
            self.file.cancelWriting()

        self.close_ui.emit()


    @Slot()
    def on_ready_read(self):
        """ Get available bytes and store them into the file """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                self.file.write(self.reply.readAll())


    @Slot()
    def on_finished(self):
        """ Delete reply, close the file, check the hash for integrity,
            extract the database and delete the downloaded zip
        """
        if self.reply:
            self.reply.deleteLater()

        if self.file:
            self.file.commit()

        self.update_status.emit("Checking DB integrity (SHA-256)")

        if match_hash(self.dest_file, self._parent.network_manager.remote_db_hash):
            self.update_status.emit("Unpacking archive...")
            delete_dir(DATA_DIR / 'SigID')
            unpack_tar(self.dest_file, DATA_DIR / 'SigID')
            delete_file(self.dest_file)
            self._parent.load_db('SigID')
            self.close_ui.emit()


    @Slot(int, int)
    def on_progress(self, bytesReceived: int):
        """ Update progress bar and label
        """
        total_bytes = self._parent.network_manager.remote_db_size
        self.update_status.emit("{:.1f} Mb / {:.1f} Mb".format(bytesReceived/10**6, total_bytes/10**6))
        self.update_progress_bar.emit(bytesReceived, total_bytes)


    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError):
        """ Show a message if an error happen during download
        """
        if self.reply:
            self.close_ui.emit()
            self.show_popup_error(
                self.reply.errorString()
            )


    def show_popup_error(self, error_msg):
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_ERROR,
            Messages.GENERIC_ERROR,
            Messages.GENERIC_ERROR_MSG.format(error_msg)
        )
