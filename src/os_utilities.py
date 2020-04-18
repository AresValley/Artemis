import sys
import platform
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
IS_RASPBIAN = IS_LINUX and 'arm' in platform.machine().lower()


def get_os():
    """Get the name of the current running operating system."""
    if IS_WINDOWS:
        return SupportedOs.WINDOWS
    elif IS_LINUX:
        if IS_RASPBIAN:
            return SupportedOs.RASPBIAN
        return SupportedOs.LINUX
    elif IS_MAC:
        return SupportedOs.MAC
    else:
        return None
