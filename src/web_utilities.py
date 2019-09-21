import os
import sys
import urllib3
from constants import Database
from executable_utilities import is_executable_version


def get_cacert_file():
    """Return the path to the cacert.pem file."""
    if is_executable_version():
        ca_certs = os.path.join(sys._MEIPASS, 'cacert.pem')
    else:
        ca_certs = 'cacert.pem'
    return ca_certs


def get_pool_manager():
    """Return a urllib3.PoolManager object."""
    return urllib3.PoolManager(ca_certs=get_cacert_file())


def download_file(url, encoding=""):
    resp = get_pool_manager().request(
        'GET',
        url,
        preload_content=True,
        timeout=4.0
    ).data
    if encoding:
        return resp.decode(encoding)
    return resp


def _download_multiline_file_as_list(url=Database.LINK_REF):
    """Download a text file and return the last line as a list.

    The downloaded file is a csv file with columns (last version == last line):
    data.zip_SHA256 | db.csv_SHA256 | Version | Creation_date"""
    try:
        f = download_file(url, encoding="UTF-8").splitlines()[-1].split(Database.DELIMITER)
    except Exception:
        return None
    return f


def get_folder_hash_code():
    return _download_multiline_file_as_list()[0]


def get_db_hash_code():
    return _download_multiline_file_as_list()[1]
