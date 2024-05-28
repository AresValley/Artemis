import os
from pathlib import Path

from artemis.utils.sql_utils import ArtemisDatabase
from artemis.utils.constants import Constants
from artemis.utils.sys_utils import *


def check_data_dir():
    if not os.path.exists(Constants.DB_DIR):
        os.makedirs(Constants.DB_DIR)


def normalize_dialog_path(path):
    if is_windows():
        norm_path = path.replace('file:///', '')
    elif is_linux() or is_macos():
        norm_path = path.replace('file:///', '/')
    return norm_path


def logs_dir():
    if is_macos():
        logs_dir_path = Path.home() / 'Library/Logs/' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME
    elif is_windows():
        logs_dir_path = Path.home() / 'AppData/Local/' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME / 'logs'
    elif is_linux():
        logs_dir_path = Path.home() / '/var/log/' / Constants.ORGANIZATION_NAME / Constants.APPLICATION_NAME
    else:
        logs_dir_path = Constants.LOGS_DIR

    if not logs_dir_path.exists():
        logs_dir_path.mkdir(parents=True)

    return logs_dir_path


def valid_db(db_dir_name):
    """ Checks if db_dir_name is a valid db dir containing a `data.sqlite` file.
        Db must be valid as well and should be properly initialized and loaded with
        no errors.

    Args:
        db_dir_name (str): name of the db folder
    """
    if os.path.exists(Constants.DB_DIR / db_dir_name / Constants.SQL_NAME):
        try:
            database = ArtemisDatabase(db_dir_name)
            database.load()
            return True
        except Exception as e:
            # Invalid or corrupted DB
            return False
    else:
        # The dir is not containing a data.sqlite file
        return False
