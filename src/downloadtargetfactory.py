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
    DownloadTarget,
    SupportedOs,
)
from os_utilities import get_os
from web_utilities import get_folder_hash_code

from zipfile import ZipFile
from tarfile import TarFile

current_os = get_os()
if current_os == SupportedOs.MAC:
    raise Exception("How to extract .dmg files?")


class _ZipExtractor:
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


class _TarExtractor:
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
    SupportedOs.WINDOWS: _ZipExtractor,
    SupportedOs.LINUX: _TarExtractor,
    SupportedOs.MAC: ...  # FIXME: Need an extractor here!
}


def _on_rmtree_error(func, path, excinfo):
    """Function called whenever rmtree fails."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _delete_data_folder():
    """Delete the Data folder."""
    if os.path.exists(Constants.DATA_FOLDER):
        rmtree(Constants.DATA_FOLDER, onerror=_on_rmtree_error)


def _delete_updater():
    """Delete the updater program."""
    if os.path.exists(Constants.UPDATER_SOFTWARE):
        remove(Constants.UPDATER_SOFTWARE)


def _delete_software():
    """Delete the main program and the themes folder."""
    if os.path.exists(Constants.EXECUTABLE_NAME):
        remove(Constants.EXECUTABLE_NAME)  # Remove Artemis executable.
    if os.path.exists(ThemeConstants.FOLDER):  # One could not have the theme folder for some reason.
        rmtree(ThemeConstants.FOLDER, onerror=_on_rmtree_error)


class _DataFolderInfo:
    """Simple class to implement the interface of a 'target' object for the data folder:

    - url;
    - hash_code;
    - size."""
    def __init__(self):
        self.url = Database.LINK_LOC
        self.hash_code = get_folder_hash_code()
        self.size = 0


class _BaseDownloadTarget:
    """Base class for the '_Download*Target' objects.

    Contains all the attributes needed by DownloadWindow and DownloadThread
    to do the job."""
    def __init__(self, target, dest_path, target_enum, Extractor, delete_files):
        self.url = target.url
        self.hash_code = target.hash_code
        self.size = target.size
        self.dest_path = dest_path
        self.target = target_enum
        self.Extractor = Extractor
        self.delete_files = delete_files


class _DownloadDataFolderTarget(_BaseDownloadTarget):
    """Extend _BaseDownloadTarget. Represent the data folder."""
    def __init__(self, data_folder_info, dest_path=__BASE_FOLDER__):
        super().__init__(
            target=data_folder_info,
            dest_path=dest_path,
            target_enum=DownloadTarget.DATA_FOLDER,
            Extractor=_ZipExtractor,
            delete_files=_delete_data_folder
        )


class _DownloadSoftwareTarget(_BaseDownloadTarget):
    """Extends _BaseDownloadTarget. Represents the main software."""
    def __init__(self, software, dest_path=__BASE_FOLDER__):
        super().__init__(
            target=software,
            dest_path=dest_path,
            target_enum=DownloadTarget.SOFTWARE,
            Extractor=EXTRACTORS[get_os()],
            delete_files=_delete_software
        )


class _DownloadUpdaterTarget(_BaseDownloadTarget):
    """Extends _BaseDownloadTarget. Represents the updater software."""
    def __init__(self, updater, dest_path=__BASE_FOLDER__):
        super().__init__(
            target=updater,
            dest_path=dest_path,
            target_enum=DownloadTarget.UPDATER,
            Extractor=EXTRACTORS[get_os()],
            delete_files=_delete_updater
        )


def get_download_target(target_type, target=None):
    """Return a Download*Obj based on the target download.

    These objects expose a common interface:
    Attributes:
    - url;
    - hash_code;
    - dest_path;
    - target: an element of the enum DownloadTarget;
    - Extractor: an object which exposes an 'open(fileobj)' method
      to extract compressed files;
    - delete_files: a function to remove the old files."""
    if target_type is DownloadTarget.DATA_FOLDER:
        return _DownloadDataFolderTarget(_DataFolderInfo())
    elif target_type is DownloadTarget.UPDATER and target is not None:
        return _DownloadUpdaterTarget(target)
    elif target_type is DownloadTarget.SOFTWARE and target is not None:
        return _DownloadSoftwareTarget(target)
    else:
        raise Exception("ERROR: Invalid download target!")
