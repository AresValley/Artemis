import uuid

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

from artemis.utils.constants import Constants, Messages
from artemis.utils.sys_utils import open_directory, make_tar, unpack_tar
from artemis.utils.sql_utils import ArtemisDatabase, ArtemisSignal
from artemis.utils.path_utils import DATA_DIR
from artemis.utils.network_utils import NetworkManager
from artemis.utils.generic_utils import generate_filter_query
from artemis.utils.path_utils import normalize_dialog_path
from artemis.utils.config_utils import CONFIGURE_QT

from artemis.ui.preferences import UIPreferences
from artemis.ui.dbmanager import UIdbmanager
from artemis.ui.signaleditor import UIsignaleditor
from artemis.ui.downloader import UIDownloader
from artemis.ui.spaceweather import UIspaceweather
from artemis.ui.documentsmanager import UIdocumentsmanager
from artemis.ui.categoryeditor import UIcategoryeditor

import artemis.resources


class UIArtemis(QObject):
    # Python > QML Signals
    populate_sig_list = Signal(list)
    populate_sig_details = Signal(list)
    populate_filter_modulation = Signal(list)
    
    clear_list = Signal()
    clear_signal_page = Signal()
    clear_filter_page = Signal()
    lock_audio_player = Signal()
    lock_menu = Signal(bool)

    show_dialog_popup = Signal(str, str, str)
    show_dialog_download_db = Signal(str, str, str)
    show_dialog_download_art = Signal(str, str, str)
    update_info_bar = Signal(str, str)


    def __init__(self):
        super().__init__()

        # Main UI initialization
        self._engine = QQmlApplicationEngine()
        self._engine.rootContext().setContextProperty('APPLICATION_VERSION', Constants.APPLICATION_VERSION)
        self._engine.rootContext().setContextProperty('PYTHON_VERSION', Constants.PYTHON_VERSION)
        self._engine.rootContext().setContextProperty('QT_VERSION', Constants.QT_VERSION)
        self._engine.load('qrc:/ui/Artemis.qml')
        self._window = self._engine.rootObjects()[0]

        self._window_filter = self._window.findChild(QObject, "filterPageObj")
        self._window_signal = self._window.findChild(QObject, "signalPageObj")

        self.loaded_db = None

        self._connect()

        # Creating istances for other windows
        self.preferences = UIPreferences(self)
        self.dbmanager = UIdbmanager(self)
        self.downloader = UIDownloader(self)
        self.spaceweather = UIspaceweather(self)
        self.docmanager = UIdocumentsmanager(self)
        self.sigeditor = UIsignaleditor(self)
        self.cateditor = UIcategoryeditor(self)

        self.network_manager = NetworkManager(self)

        self.autoload_db()


    def _connect(self):
        # QML > Python connections
        self._window.showDBmanager.connect(self.show_dbmanager_ui)
        self._window.loadSignal.connect(self.load_sig)
        self._window.showPref.connect(self.show_pref_ui)
        self._window.openSigEditor.connect(self.open_sig_editor)
        self._window.startDownloader.connect(self.start_download_db)
        self._window.checkDbUpdates.connect(self.check_update_db)
        self._window.showSpaceWeather.connect(self.show_space_weather_ui)
        self._window.openDbDirectory.connect(self.open_db_directory)
        self._window.showCatManager.connect(self.open_cat_manager)
        
        self._window.newDb.connect(self.new_db)
        self._window.exportDb.connect(self.export_db)
        self._window.importDb.connect(self.import_db)

        self._window_filter.applyFilter.connect(self.apply_filter)
        self._window_filter.sendBottomAlert.connect(self.bottom_info_bar)

        self._window_signal.openDocManager.connect(self.show_documentsmanager_ui)
        self._window_signal.openSigEditor.connect(self.open_sig_editor)
        self._window_signal.deleteCatTag.connect(self.delete_cat_tag)
        self._window_signal.addCatTag.connect(self.add_cat_tag)

        # Python > QML connections
        self.populate_sig_list.connect(self._window.populateList)
        self.clear_list.connect(self._window.clearList)
        self.update_info_bar.connect(self._window.bottomInfoBar)
        self.show_dialog_popup.connect(self._window.openGeneralDialog)
        self.show_dialog_download_db.connect(self._window.openDialogDownloadDb)
        self.show_dialog_download_art.connect(self._window.openDialogDownloadArtemis)
        self.lock_menu.connect(self._window.lockMenu)

        self.populate_sig_details.connect(self._window_signal.populateSignalParam)
        self.lock_audio_player.connect(self._window_signal.lockPlayer)
        self.clear_signal_page.connect(self._window_signal.resetAll)
        
        self.clear_filter_page.connect(self._window_filter.resetAll)
        self.populate_filter_modulation.connect(self._window_filter.loadLists)


    def load_db(self, db_dir_name):
        """ Load the DB and populate the signals list

        Args:
            db_dir_name (str): folder name in the data folder
        """
        # Loading DB
        self.loaded_db = ArtemisDatabase(db_dir_name)
        self.loaded_db.load()
        # Clearing UI
        self.lock_menu.emit(False)
        self.clear_signal_page.emit()
        self.clear_filter_page.emit()
        # Populating UI
        self.load_filter_lists()
        self.populate_sig_list.emit(self.loaded_db.all_signals)
        # Updating status bar
        total_signals = len(self.loaded_db.all_signals)
        self.bottom_info_bar("Database loaded with {} signals".format(total_signals), "info")


    @Slot(int)
    def load_sig(self, sig_id):
        """ Load the selected signal and populate the SignalPage

        Args:
            sig_id (int): SIG_ID of the signal to be loaded 
        """
        self.loaded_sig = ArtemisSignal(self.loaded_db)
        self.loaded_sig.load(sig_id)
        sig_dic = self.loaded_sig.generate_dic()

        self.populate_sig_details.emit([sig_dic])


    def load_filter_lists(self):
        """ Populates the 3 listviews in the FilterPage
        """
        self.populate_filter_modulation.emit([{
            'modulation': self.loaded_db.all_modulation,
            'location': self.loaded_db.all_location,
            'category': self.loaded_db.all_category_labels
        }])


    @Slot(dict)
    def apply_filter(self, filter_status):
        """ Update the signal list according to the selected filters in the FilterPage.

        Args:
            filter_status (dic): dictionary containing the active filters with all
            the details to generate a search query
        """
        filter_status = filter_status.toVariant()
        if self.loaded_db is not None:
            if filter_status != {}:
                filter_query = generate_filter_query(filter_status)
                self.loaded_db.select_by_filter(filter_query)
                
                self.clear_signal_page.emit()
                self.populate_sig_list.emit(self.loaded_db.all_signals)

                total_signals = len(self.loaded_db.all_signals)
                self.bottom_info_bar("FILTERS ACTIVE: {} signals found".format(total_signals), "warning")
            else:
                self.load_db(self.loaded_db.db_dir_name)


    def show_pref_ui(self):
        """ Load the preference windows
        """
        self.preferences.load_preferences_ui()


    def show_dbmanager_ui(self):
        """ Load the DB manager windows
        """
        self.dbmanager.load_dbmanager_ui()


    @Slot(str, list, bool)
    def open_sig_editor(self, type, sig_param, is_new):
        """ Open the signal editor windows
            Called when the user want to add, edit or delete the signal or its parametes.
        """
        self.sigeditor.load_signaleditor_ui(type, sig_param, is_new)


    def show_space_weather_ui(self):
        """ Open the space weather windows
        """
        self.spaceweather.load_spaceweather_ui()


    def show_documentsmanager_ui(self):
        """ Open the documents manager windows
        """
        self.docmanager.load_documentsmanager_ui()


    def check_update_db(self):
        """ User manual check for updates db updates
        """
        self.network_manager.show_popup = True
        self.network_manager.check_updates()


    def start_download_db(self):
        """ Show the downloader and start the download of the sigid db
        """
        self.downloader.show_ui.emit()
        self.downloader.on_start()


    def dialog_download_db(self, message_type, title, message):
        """ Dialog popup for DB download confirmation
        """
        self.show_dialog_download_db.emit(message_type, title, message)


    def dialog_download_artemis(self, message_type, title, message):
        """ Dialog popup for artemis download confirmation
        """
        self.show_dialog_download_art.emit(message_type, title, message)


    def open_db_directory(self):
        """ Open the local folder of the loaded DB
        """
        open_directory(self.loaded_db.db_dir)


    @Slot(str)
    def new_db(self, name):
        """ Create a new local DB

        Args:
            name (str): name of the new DB, hardcoded in sql info table
        """
        try:
            new_db = ArtemisDatabase(str(uuid.uuid4()))
            new_db.create(name)
            self.load_db(new_db.db_dir_name)
            self.dialog_popup(
                Messages.DIALOG_TYPE_INFO,
                Messages.GENERIC_SUCCESS,
                Messages.DB_CREATION_SUCCESS_MSG
            )
        except Exception as e:
            self.dialog_popup(
                Messages.DIALOG_TYPE_ERROR,
                Messages.GENERIC_ERROR,
                Messages.GENERIC_ERROR_MSG.format(e)
            )


    @Slot(str)
    def export_db(self, save_path):
        """ Export the load DB in a tar file. Does not use compression

        Args:
            save_path (str): destination path of the generated .tar file
        """
        try:
            dest_path = normalize_dialog_path(save_path)
            make_tar(dest_path, self.loaded_db.db_dir)
            self.dialog_popup(
                Messages.DIALOG_TYPE_INFO,
                Messages.GENERIC_SUCCESS,
                Messages.EXPORTING_SUCCESS_MSG
            )
        except Exception as e:
            self.dialog_popup(
                Messages.DIALOG_TYPE_ERROR,
                Messages.GENERIC_ERROR,
                Messages.GENERIC_ERROR_MSG.format(e)
            )


    @Slot(str)
    def import_db(self, tar_path):
        """ Import a new DB in the Artemis data folder

        Args:
            tar_path (str): Path of the archive to be imported
        """
        try:
            origin_path = normalize_dialog_path(tar_path)
            save_path = DATA_DIR / str(uuid.uuid4())
            unpack_tar(origin_path, save_path)
            self.dialog_popup(
                Messages.DIALOG_TYPE_INFO,
                Messages.GENERIC_SUCCESS,
                Messages.IMPORTING_SUCCESS_MSG
            )
        except Exception as e:
            self.dialog_popup(
                Messages.DIALOG_TYPE_ERROR,
                Messages.GENERIC_ERROR,
                Messages.GENERIC_ERROR_MSG.format(e)
            )


    @Slot(int)
    def add_cat_tag(self, clb_id):
        self.loaded_sig.insert_category(clb_id)
        self.load_db(self.loaded_db.db_dir_name)


    @Slot(int)
    def delete_cat_tag(self, cat_id):
        self.loaded_sig.delete_category(cat_id)
        self.load_db(self.loaded_db.db_dir_name)


    def open_cat_manager(self):
        """ Open the category manager windows
        """
        self.cateditor.load_cateditor_ui()


    def autoload_db(self):
        sig_id_path = DATA_DIR / 'SigID' / Constants.SQL_NAME
        autoload = CONFIGURE_QT.value("Database", "autoload", 0)
        if sig_id_path.exists() and int(autoload):
            self.load_db('SigID')


    def dialog_popup(self, message_type, title, message):
        """ Opens a general dialog popup

        Args:
            message_type (str): 'info', 'question', 'warn', 'error'
            title (str): header of the dialoog
            message (sstr): description inside the dialog
        """
        self.show_dialog_popup.emit(message_type, title, message)


    @Slot(str, str)
    def bottom_info_bar(self, message, message_type):
        """ Manage the footer info bar

        Args:
            message (str): text to be shown in the info bar
            message_type (str): 'info', 'warning'
        """
        self.update_info_bar.emit(message, message_type)
