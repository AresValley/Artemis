import os
from pathlib import Path

from artemis.utils.constants import Constants
from artemis.utils.sys_utils import is_windows, is_linux, is_macos


def normalize_dialog_path(path):
    if is_windows():
        norm_path = path.replace('file:///', '')
    elif is_linux() or is_macos():
        norm_path = path.replace('file:///', '/')
    return norm_path


def _app_dir():
    if is_macos():
        app_dir_path = Path.home() / 'Library' / 'Application Support' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME
    elif is_windows():
        app_dir_path = Path.home() / 'AppData' / 'Local' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME
    elif is_linux():
        app_dir_path = Path.home() / '.local' / 'share' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME
    else:
        app_dir_path = BASE_DIR

    if not app_dir_path.exists():
        app_dir_path.mkdir(parents=True)

    return app_dir_path


def _data_dir():
    data_dir_path = APP_DIR / 'data'
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)
    return data_dir_path


def _preference_dir():
    preference_dir_path = APP_DIR / 'config'
    if not preference_dir_path.exists():
        preference_dir_path.mkdir(parents=True)
    return preference_dir_path    


BASE_DIR = Path(os.path.dirname(__file__)) / '../..'
APP_DIR = _app_dir()
DATA_DIR = _data_dir()
PREFERENCES_DIR = _preference_dir()
