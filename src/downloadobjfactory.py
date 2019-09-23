from contextlib import contextmanager
from shutil import rmtree
from os import remove
import os.path
import stat

from constants import (
    Constants,
    Database,
    __BASE_FOLDER__,
    ThemeConstants,
    DownloadObj,
    SupportedOs,
)
from os_utilities import get_os
from web_utilities import get_folder_hash_code
from versioncontroller import version_controller

from zipfile import ZipFile
from tarfile import TarFile

current_os = get_os()
if current_os == SupportedOs.MAC:
    raise Exception("How to extract .dmg files?")


class ZipExtractor:
    """Extractor class for zip files.

    Exposes a static method which can be used as a context manager."""
    @staticmethod
    @contextmanager
    def open(fileobj):
        zipped = ZipFile(fileobj)
        try:
            yield zipped
        finally:
            zipped.close()


class TarExtractor:
    """Extractor class for tar files.

    Exposes a static method which can be used as a context manager."""
    @staticmethod
    @contextmanager
    def open(fileobj):
        tarfile = TarFile.open(fileobj=fileobj)
        try:
            yield tarfile
        finally:
            tarfile.close()


EXTRACTORS = {
    SupportedOs.WINDOWS: ZipExtractor,
    SupportedOs.LINUX: TarExtractor,
    SupportedOs.MAC: ...  # FIXME: Need an extractor here!
}


def on_rmtree_error(func, path, excinfo):
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
        self.Extractor = ZipExtractor

    def delete_files(self):
        if os.path.exists(Constants.DATA_FOLDER):
            rmtree(Constants.DATA_FOLDER, onerror=on_rmtree_error)


class _DownloadSoftwareObj:
    def __init__(self):
        self.url = version_controller.software.url
        self.hash_code = version_controller.software.hash_code
        self.size = version_controller.software.size
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.SOFTWARE
        self.Extractor = EXTRACTORS[get_os()]

    def delete_files(self):
        if os.path.exists(Constants.EXECUTABLE_NAME):
            remove(Constants.EXECUTABLE_NAME)  # Remove Artemis executable.
        if os.path.exists(ThemeConstants.FOLDER):  # One could not have the theme folder for some reason.
            rmtree(ThemeConstants.FOLDER, onerror=on_rmtree_error)


class _DownloadUpdaterObj:
    def __init__(self):
        self.url = version_controller.updater.url
        self.hash_code = version_controller.updater.hash_code
        self.size = version_controller.updater.size
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.UPDATER
        self.Extractor = EXTRACTORS[get_os()]

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
    - target: an element of the enum DownloadObj;
    - Extractor: an object which exposes an 'open(fileobj) method
      to extract compressed files.
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
