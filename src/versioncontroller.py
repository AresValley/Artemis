from io import BytesIO
import json
from constants import Constants
from os_utilities import get_os
from web_utilities import download_file


"""This module exposes just one class: VersionController.

All the relevant information can be accessed with the dot notation on an instance of such class, e.g.:
               version_controller.software.hash_code
is the hash_code of the latest release of the software running on the current OS."""


def _download_versions_file():
    """Download the json file containing all the information
    about the latest version of the software. Return a dictionary
    containing only the information for the running OS.

    Return a dictionary from a json with the following structure:
    {
        "windows": {
            "software": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            },
            "updater": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            }
        },
        "linux": {
            "software": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            },
            "updater": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            }
        },
        "mac": {
            "software": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            },
            "updater": {
                "version": "...",
                "url": "...",
                "hash_code": "...",
                "size": ...
            }
        }
    }
    """
    try:
        version_dict = json.load(
            BytesIO(download_file(Constants.VERSION_LINK))
        )[get_os()]
    except Exception:
        return None
    else:
        return version_dict


class VersionController:
    """Dynamically create attributes corresponding to elements of a dictionary.

    Used to get updates information."""

    def __init__(self, dct=None):
        """Initialize the dictionary"""
        super().__init__()
        self._dct = dct

    def __getattr__(self, attr):
        """Override super().__getattr__. Dynamically create new attributes
        corresponding to elements of the diciotnary."""
        if self._dct is None:
            if not self.update():
                return None
        try:
            dct_element = self._dct[attr]
        except Exception("ERROR: Invalid attribute!"):
            return None
        else:
            if isinstance(dct_element, dict):
                setattr(self, attr, type(self)(dct_element))
            else:
                setattr(self, attr, dct_element)
            return getattr(self, attr)

    def update(self):
        """Reset the dictionary to the correspondig json file containing
        the latest version information. Call this function inside a Qthread."""
        dct = _download_versions_file()
        if dct is not None:
            self._dct = dct
            return True
        else:
            return False
