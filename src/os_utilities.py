import sys
from constants import SupportedOs


def _is_mac_os():
    """Return True if running OS is Mac."""
    return sys.platform == 'darwin'


def _is_win_os():
    """Return True if running OS is Windows."""
    return sys.platform == 'win32'


def _is_linux_os():
    """Return True if running OS is Linux."""
    return sys.platform == 'linux'


IS_MAC = _is_mac_os()
IS_LINUX = _is_linux_os()
IS_WINDOWS = _is_win_os()


def get_os():
    """Get the name of the current running operating system."""
    if IS_WINDOWS:
        return SupportedOs.WINDOWS
    elif IS_LINUX:
        return SupportedOs.LINUX
    elif IS_MAC:
        return SupportedOs.MAC
    else:
        raise Exception("ERROR: OS not recognized.")
