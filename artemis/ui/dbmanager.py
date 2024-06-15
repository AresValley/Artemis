import os

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

from artemis.utils.path_utils import DATA_DIR
from artemis.utils.generic_utils import *
from artemis.utils.sql_utils import ArtemisDatabase
from artemis.utils.sys_utils import delete_dir


class UIdbmanager(QObject):
    # Python > QML Signals
    show_ui = Signal()
    close_ui = Signal()
    populate_db_list = Signal(list)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/DbManager.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.loadDB.connect(self.load_db)
        self._window.deleteDB.connect(self.delete_db)
        self._window.renameDB.connect(self.rename_db)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.close_ui.connect(self._window.close)
        self.populate_db_list.connect(self._window.loadList)


    def load_dbmanager_ui(self):
        self.load_local_db_list()
        self.show_ui.emit()


    def load_local_db_list(self):
        """ Scan for all the valid DBs in the data folder and show them on the list
        """
        db_param = []
        valid_db_list = self.scan_db_dir()

        for db in valid_db_list:
            db_param.append(
                {
                    'name': db.name,
                    'version': db.version,
                    'date': parse_date(db.date),
                    'db_dir_name': db.db_dir_name,
                    'documents_n': db.stats['documents'],
                    'signals_n': db.stats['signals'],
                    'images_n': db.stats['images'],
                    'audio_n': db.stats['audio']
                }
            )

        self.populate_db_list.emit(db_param)


    def load_db(self, db_dir_name):
        """ Load the selected DB (from the DB Manager list) in the main artemis window
        """
        self._parent.load_db(db_dir_name)
        self.close_ui.emit()


    @Slot(str)
    def delete_db(self, db_dir_name):
        """ Delete the DB folder.
            Clear the main UI if the database to be deleted is the selected one 
        """
        if self._parent.loaded_db is not None:
            if self._parent.loaded_db.db_dir_name == db_dir_name:
                self._parent.lock_menu.emit(True)
                self._parent.clear_list.emit()
                self._parent.clear_signal_page.emit()
        delete_dir(DATA_DIR / db_dir_name)
        self.load_local_db_list()


    @Slot(str, str)
    def rename_db(self, db_dir_name, new_name):
        """ Rename db in the data folder
        """
        database = ArtemisDatabase(db_dir_name)
        database.rename(new_name)
        self.load_local_db_list()


    def scan_db_dir(self):
        """ Scans the data directory for valid databases and
            return a dictionary containing only the valid ones.
            Returns a list of objects (dbs)
        """
        valid_db_list = []
        db_dirs = next(os.walk(DATA_DIR))[1]

        for db_dir_name in db_dirs:
            try:
                database = ArtemisDatabase(db_dir_name)
                database.load()
                valid_db_list.append(database)
            except:
                continue

        return valid_db_list


    def get_latest_local_sigid_db(self):
        """ Return the newest valid local sigID database.
            Returns None if no valid sigID database is found.
        """
        valid_dbs = self._parent.dbmanager.scan_db_dir()
        sig_id_dbs = [db for db in valid_dbs if db.editable == -1]

        if len(sig_id_dbs) != 0:
            sig_id_latest = max(sig_id_dbs, key=lambda x: x.version)
            return sig_id_latest
        else:
            return None
