import sys
from constants import SupportedOs


def is_mac_os():
    """Return True if running OS is Mac."""
    return sys.platform == 'darwin'


def is_win_os():
    """Return True if running OS is Windows."""
    return sys.platform == 'win32'


def is_linux_os():
    """Return True if running OS is Linux."""
    return sys.platform == 'linux'


def get_os():
    """Get the name of the current running operating system."""
    if is_win_os():
        return SupportedOs.WINDOWS
    elif is_linux_os():
        return SupportedOs.LINUX
    elif is_mac_os():
        return SupportedOs.MAC
    else:
        raise Exception("ERROR: OS not recognized.")
