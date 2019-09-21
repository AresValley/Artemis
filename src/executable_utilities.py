import sys
from shutil import which
import os
import os.path


def is_executable_version():
    """Return whether the binary version is running."""
    return hasattr(sys, "_MEIPASS")


def get_executable_path():
    """Check whether the executable is in the PATH folder.

    Return the full path or just an ampty string if it is not found
    in the PATH folder."""
    path = which("Artemis")
    if path is not None:
        return os.path.dirname(path)
    else:  # Assume that the executable is in the cwd.
        return os.curdir


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
