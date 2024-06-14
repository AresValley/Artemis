import os
import uuid
import requests

from packaging.version import Version

from artemis.utils.constants import Constants, Messages
from artemis.utils.sql_utils import ArtemisDatabase
from artemis.utils.sys_utils import is_windows, is_linux, is_macos, delete_file, delete_dir, match_hash, unpack_tar, open_file
from artemis.utils.path_utils import DATA_DIR, TMP_DIR


class UpdateManager:
    """ Class used to manage DB and software updates
    """

    def __init__(self, parent):
        self._parent = parent

        self.db_update = None
        self.art_update = None

        self.remote_db_url = None
        self.remote_db_hash = None
        self.remote_db_version = None
        self.remote_db_size = None
        self.remote_db_file_name = None

        self.remote_artemis_version = None
        self.remote_artemis_url = None
        self.remote_artemis_file_name = None

        self.check_updates()


    def check_updates(self, show_popup=False):
        """ Checks if a software or DB update is available.
            Prioritize Artemis updates over the DB one.

            Args:
                show_popup (bool, optional): 
                    If False, suppress the "already up-to-date" message on startup.
                    Defaults to False. True is usefull when the user manual check for
                    updates.
        """
        latest_json = self.fetch_remote_json(Constants.LATEST_VERSION_URL, show_popup)
        if latest_json:
            local_db = self._parent.dbmanager.get_latest_local_sigid_db()
            remote_db = latest_json['sigID_DB']

            self.remote_db_version = remote_db['version']
            self.remote_db_url = remote_db['url']
            self.remote_db_hash = remote_db['sha256_hash']
            self.remote_db_size = remote_db['total_bytes']
            self.remote_db_file_name = self.remote_db_url.split('/')[-1]

            if is_windows():
                self.remote_artemis_version = latest_json['windows']['version']
                self.remote_artemis_url = latest_json['windows']['url']
            elif is_linux():
                self.remote_artemis_version = latest_json['linux']['version']
                self.remote_artemis_url = latest_json['linux']['url']
            elif is_macos():
                self.remote_artemis_version = latest_json['mac']['version']
                self.remote_artemis_url = latest_json['mac']['url']
            
            self.remote_artemis_file_name = self.remote_artemis_url.split('/')[-1]

            if Version(self.remote_artemis_version) > Version(Constants.APPLICATION_VERSION):
                self.art_update = True
            else:
                self.art_update = False         

            if self.art_update:
                self._show_popup_art_update()
            else:
                if local_db:
                    if self.remote_db_version > local_db.version:
                        self._show_popup_db_update()
                    elif show_popup:
                        self._show_popup_up_to_date()
                else:
                    self._show_popup_initial_db_download()


    def fetch_remote_json(self, url, show_popup=False):
        """ Fetches the remote json from a url

            Args:
                show_popup (bool, optional): If false, suppress any error message
                Defaults to False (to avoid error if the program is used offline)
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if show_popup:
                self._parent.dialog_popup(
                    Messages.DIALOG_TYPE_ERROR,
                    Messages.NO_CONNECTION,
                    Messages.NO_CONNECTION_MSG.format(e)
                )
            return None


    def download_db(self):
        """ Open the downloader and download the sigID database in the 
            TMP_DIR folder. After a succesfull download the callback function
            from the downloader is post_download_db
        """
        self._parent.downloader.finished.connect(self.post_download_db)
        self._parent.downloader.on_start(
            self.remote_db_url,
            TMP_DIR
        )


    def post_download_db(self):
        """ After a succesfull DB download, this function check the hash
            for possible corrupted data, delete old sigID DB and extract
            the new one
        """
        latest_db_tar_path = TMP_DIR / self.remote_db_file_name
        if match_hash(latest_db_tar_path, self.remote_db_hash):
            db_dir_name = str(uuid.uuid4())
            unpack_tar(latest_db_tar_path, DATA_DIR / db_dir_name)
            self._parent.load_db(db_dir_name)
            self._show_popup_db_download_complete()
        else:
            self._show_popup_db_hash_failed()
        delete_file(latest_db_tar_path)


    def download_artemis(self):
        """ Open the downloader and download Artemis in the 
            TMP_DIR folder. After a succesfull download the callback function
            from the downloader is post_download_artemis
        """
        self._parent.downloader.finished.connect(self.post_download_artemis)
        self._parent.downloader.on_start(
            self.remote_artemis_url,
            TMP_DIR
        )


    def post_download_artemis(self):
        """ After a succesfull Artemis download, this open the installer
            and close the application
        """
        if is_windows():
            open_file(TMP_DIR / self.remote_artemis_file_name)
            self._parent.close_ui.emit()


    def _show_popup_db_update(self):
        """ Prompts the user to download the updated version of the database
        """
        self._parent.dialog_download_db(
            Messages.DIALOG_TYPE_WARN,
            Messages.DB_NEW_VER,
            Messages.DB_NEW_VER_MSG.format(self.remote_db_version)
        )


    def _show_popup_art_update(self):
        """ Alerts the user of a new version of Artemis.
            Windows - asks to download with automatic update
            Linux, macOS - redirects to GitHub page
        """
        if is_windows():
            self._parent.dialog_update_artemis(
                Messages.DIALOG_TYPE_QUEST,
                Messages.ART_NEW_VER,
                Messages.ART_NEW_VER_AUTO_MSG.format(self.remote_artemis_version),
                True
            )
        else:
            self._parent.dialog_update_artemis(
                Messages.DIALOG_TYPE_QUEST,
                Messages.ART_NEW_VER,
                Messages.ART_NEW_VER_MANUAL_MSG.format(self.remote_artemis_version),
                False
            )


    def _show_popup_up_to_date(self):
        """ Notifies the user that the database is up to date
        """
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_INFO,
            Messages.UP_TO_DATE,
            Messages.UP_TO_DATE_MSG
        )


    def _show_popup_initial_db_download(self):
        """ Prompts the user to download the database for the first time
        """
        self._parent.dialog_download_db(
            Messages.DIALOG_TYPE_QUEST,
            Messages.NO_DB_DETECTED,
            Messages.NO_DB_DETECTED_MSG
        )


    def _show_popup_db_download_complete(self):
        """ DB has been succesfully downloaded
        """
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_INFO,
            Messages.GENERIC_SUCCESS,
            Messages.DB_DOWNLOAD_SUCCESS_MSG
        )


    def _show_popup_db_hash_failed(self):
        """ Notify the user after detection of a corrupted database
        """
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_ERROR,
            Messages.DB_CORRUPTED,
            Messages.DB_CORRUPTED_MSG
        )
