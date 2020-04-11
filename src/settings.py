import os.path
from constants import Constants
import json
import logging


class Settings:
    """Dynamically save and load the settings of the application."""

    def __init__(self):
        self._dct = {}

    def load(self):
        """Load the setiings.json file."""
        if not os.path.exists(Constants.SETTINGS_FILE):
            return
        try:
            with open(Constants.SETTINGS_FILE, 'r') as settings_file:
                self._dct = json.load(settings_file)
        except FileNotFoundError:
            logging.info("No settings.json file")
            pass  # Invalid file.

    def save(self, **kwargs):
        """Save the settings.json file.

        Also update the current settings specified in kwargs.
        New settings can be dynamically added via this method."""
        for k, v in kwargs.items():
            self._dct[k] = v
        with open(Constants.SETTINGS_FILE, mode='w') as settings_file:
            json.dump(
                self._dct,
                settings_file,
                sort_keys=True,
                indent=4
            )

    def __getattr__(self, attr):
        """Return the corresponding setting.

        Return None if there is no such setting yet."""
        return self._dct.get(attr, None)
