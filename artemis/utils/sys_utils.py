import os
import platform
import subprocess
import hashlib

from shutil import rmtree, copyfile, make_archive, unpack_archive
from pathlib import Path

from artemis.utils.constants import Constants, Messages


def is_windows():
    return platform.system() == 'Windows'

def is_macos():
    return platform.system() == 'Darwin'

def is_linux():
    return platform.system() == 'Linux'


def open_file(file_path, timeout=3):
    try:
        if is_windows():
            os.startfile(file_path)
        elif is_macos():
            subprocess.call(['open', file_path], timeout=timeout)
        elif is_linux():
            subprocess.call(['xdg-open', file_path], timeout=timeout)
        else:
            return
    except FileNotFoundError:
        raise Exception(Messages.FILE_NOT_FOUND_ERR_MSG)
    except Exception as e:
        raise Exception(Messages.GENERIC_ERROR_MSG.format(e))


def open_directory(directory, timeout=3):
    if is_windows():
        subprocess.call(['explorer', str(Path(directory))], timeout=timeout)
    elif is_macos():
        subprocess.call(['open', directory], timeout=timeout)
    elif is_linux():
        subprocess.call(['xdg-open', directory], timeout=timeout)
    else:
        return


def delete_db_dir(db_dir_name):
    """Delete the db folder"""
    db_dir = Constants.DB_DIR / db_dir_name
    if os.path.exists(db_dir):
        rmtree(db_dir)


def copy_file(src_file_path, dst_file_path):
    copyfile(src_file_path, dst_file_path)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path) 


def pack_db(save_path, db_dir):
    make_archive(save_path, 'tar', db_dir.resolve().as_posix())


def unpack_db(tar_path, db_dir_name):
    db_dir = Constants.DB_DIR / db_dir_name
    unpack_archive(tar_path, db_dir, 'tar')


def match_hash(data, reference_hash):
    """ Check whether the checksum of 'data' match the reference one.

    Args:
        data (str): Path of the file to be checked
        reference_hash (str): Reference SHA-256 hash
    """
    if reference_hash is None:
        raise ValueError("ERROR: Invalid hash code.")

    code = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(data, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            code.update(mv[:n])

    return code.hexdigest() == reference_hash
