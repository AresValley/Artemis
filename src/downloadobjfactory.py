from shutil import rmtree
from os import remove
import os.path
import stat
from constants import (
    Constants,
    Database,
    __BASE_FOLDER__,
    ThemeConstants,
    DownloadObj
)
from web_utilities import get_folder_hash_code
from versioncontroller import version_controller


def _on_rmtree_error(func, path, excinfo):
    """Function called whenever rmtree fails."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


class _DownloadFolderObj:
    def __init__(self):
        self.url = Database.LINK_LOC
        self.hash_code = get_folder_hash_code()
        self.size = 0
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.FOLDER

    def delete_files(self):
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER, onerror=_on_rmtree_error)


class _DownloadSoftwareObj:
    def __init__(self):
        self.url = version_controller.software.url
        self.hash_code = version_controller.software.hash_code
        self.size = version_controller.software.size
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.SOFTWARE

    def delete_files(self):
        if os.path.exists(Constants.EXECUTABLE_NAME):
            remove(Constants.EXECUTABLE_NAME)  # Remove Artemis executable.
        if os.path.exists(ThemeConstants.FOLDER):  # One could not have the theme folder for some reason.
            rmtree(ThemeConstants.FOLDER, onerror=_on_rmtree_error)


class _DownloadUpdaterObj:
    def __init__(self):
        self.url = version_controller.updater.url
        self.hash_code = version_controller.updater.hash_code
        self.size = version_controller.updater.size
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.UPDATER

    def delete_files(self):
        if os.path.exists(Constants.UPDATER_SOFTWARE):
            remove(Constants.UPDATER_SOFTWARE)


def get_download_target(obj_type):
    """Return a Download*Obj based on the target download.

    These objects expose a common interface:
    Attributes:
    - url;
    - hash_code;
    - dest_path;
    - target: an element of the enum DownloadObj.
    Methods:
    - delete_files()"""
    if obj_type is DownloadObj.FOLDER:
        return _DownloadFolderObj()
    elif obj_type is DownloadObj.UPDATER:
        return _DownloadUpdaterObj()
    elif obj_type is DownloadObj.SOFTWARE:
        return _DownloadSoftwareObj()
    else:
        raise Exception("ERROR: Invalid download target!")
