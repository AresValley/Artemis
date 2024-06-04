from configparser import ConfigParser

from artemis.utils.path_utils import PREFERENCES_DIR, BASE_DIR
from artemis.utils.sys_utils import copy_file


class Config(ConfigParser):
    """ Custom configuration class derived from ConfigParser.
        Used to get, set, save and remove any configuration from the conf file
    """

    def __init__(self, config_file_path, space_around_delimiters=False):
        super().__init__()
        self._config_file_path = config_file_path
        self.read(self._config_file_path)
        self._space_around_delimiters = space_around_delimiters

    def get_or_default(self, section, option, default_value):
        value = super().get(section, option)
        return value if value else default_value

    def set(self, section, option, value=None):
        super().set(section, option, value)
        self.save()

    def remove(self, section, option):
        super().remove_option(section, option)
        self.save()

    def save(self):
        with open(self._config_file_path, 'w') as f:
            self.write(f, space_around_delimiters=self._space_around_delimiters)


if not (PREFERENCES_DIR / 'qtquickcontrols2.conf').exists():
    copy_file(
        BASE_DIR / 'config' / 'qtquickcontrols2.conf',
        PREFERENCES_DIR / 'qtquickcontrols2.conf'
    )

CONFIGURE_QT = Config((PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve().as_posix())
