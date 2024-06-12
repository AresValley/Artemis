import os
import requests

from packaging.version import Version

from artemis.utils.constants import Constants, Messages
from artemis.utils.sql_utils import ArtemisDatabase
from artemis.utils.sys_utils import is_windows, is_linux, is_macos, delete_file, delete_dir, match_hash, unpack_tar
from artemis.utils.path_utils import DATA_DIR


class UpdateManager:
    """ Class used to manage DB and software updates
    """

    def __init__(self, parent):
        self._parent = parent
        self.sigid_db_path = DATA_DIR / 'SigID' / Constants.SQL_NAME

        self.db_update = None
        self.art_update = None

        self.remote_db_url = None
        self.remote_db_hash = None
        self.remote_db_version = None
        self.remote_db_size = None
        self.remote_db_file_name = None

        self.remote_art_version = None

        self.check_updates()


    def check_updates(self, show_popup=False):
        """ Checks if a software or DB update is available.
            Prioritize Artemis update over DB one.

            Args:
                show_popup (bool, optional): 
                    Suppress the "already up-to-date" message on startup.
                    Defaults to False.
        """
        latest_json = self._fetch_remote_json(Constants.LATEST_VERSION_URL, show_popup)
        if latest_json:
            local_db = self._load_local_db()
            remote_db = latest_json['sigID_DB']

            self.remote_db_version = remote_db['version']
            self.remote_db_url = remote_db['url']
            self.remote_db_hash = remote_db['sha256_hash']
            self.remote_db_size = remote_db['total_bytes']
            self.remote_db_file_name = self.remote_db_url.split('/')[-1]

            if is_windows():
                self.remote_art_version = latest_json['windows']['version']
            elif is_linux():
                self.remote_art_version = latest_json['linux']['version']
            elif is_macos():
                self.remote_art_version = latest_json['mac']['version']

            if Version(self.remote_art_version) > Version(Constants.APPLICATION_VERSION):
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


    def _fetch_remote_json(self, url, show_popup=False):
        """ Fetches the remote json from a url
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


    def _load_local_db(self):
        """ Loads the local database if exists
        """
        if os.path.exists(self.sigid_db_path):
            local_db = ArtemisDatabase('SigID')
            local_db.load()
            return local_db
        return None
    

    def post_download_db(self):
        latest_db_tar_path = DATA_DIR / self.remote_db_file_name
        if match_hash(latest_db_tar_path, self.remote_db_hash):
            delete_dir(DATA_DIR / 'SigID')
            unpack_tar(latest_db_tar_path, DATA_DIR / 'SigID')
            self._parent.load_db('SigID')
            self._show_popup_db_download_complete()
        else:
            self._show_popup_db_hash_failed()
        delete_file(latest_db_tar_path)


    def _show_popup_db_update(self):
        """ Prompts the user to download the updated version of the database.
        """
        self._parent.dialog_download_db(
            Messages.DIALOG_TYPE_WARN,
            Messages.DB_NEW_VER,
            Messages.DB_NEW_VER_MSG.format(self.remote_db_version)
        )


    def _show_popup_art_update(self):
        """ Prompts the user to download the updated version of the database.
        """
        self._parent.dialog_download_artemis(
            Messages.DIALOG_TYPE_WARN,
            Messages.ART_NEW_VER,
            Messages.ART_NEW_VER_MSG.format(self.remote_art_version)
        )


    def _show_popup_up_to_date(self):
        """ Notifies the user that the database is up to date.
        """
        self._parent.dialog_popup(
            Messages.DIALOG_TYPE_INFO,
            Messages.UP_TO_DATE,
            Messages.UP_TO_DATE_MSG
        )


    def _show_popup_initial_db_download(self):
        """ Prompts the user to download the database for the first time.
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
