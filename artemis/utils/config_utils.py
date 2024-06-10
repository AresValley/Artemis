from configparser import ConfigParser

from artemis.utils.path_utils import PREFERENCES_DIR, BASE_DIR
from artemis.utils.sys_utils import copy_file


class Config(ConfigParser):
    """ Custom configuration class derived from ConfigParser.
        Used to get value, set, save and remove any configuration from the conf file
    """

    def __init__(self, config_file_path, space_around_delimiters=False):
        super().__init__()
        self._config_file_path = config_file_path
        self.read(self._config_file_path)
        self._space_around_delimiters = space_around_delimiters

    def value(self, section, option, default_value):
        value = super().get(section, option, fallback=default_value)
        return value

    def set(self, section, option, value=None):
        if not self.has_section(section):
            self.add_section(section)
        super().set(section, option, value)
        self.save()

    def remove(self, section, option):
        super().remove_option(section, option)
        self.save()

    def save(self):
        with open(self._config_file_path, 'w') as f:
            self.write(f, space_around_delimiters=self._space_around_delimiters)


def merge_config_files(old_config_path, template_config_path):
    """ Merge two configuration files: if the old one lacks some
        sections or options from a comparison with a template,
        this function will add what is missing to the old conf file
    """
    old_config = ConfigParser()
    old_config.read(old_config_path)
    
    new_config = ConfigParser()
    new_config.read(template_config_path)
    
    for section in new_config.sections():
        if not old_config.has_section(section):
            old_config.add_section(section)
        for option in new_config.options(section):
            if not old_config.has_option(section, option):
                old_config.set(section, option, new_config.get(section, option))
    
    with open(old_config_path, 'w') as f:
        old_config.write(f)


def check_conf_file():
    """ Check the integrity of the used conf file.
        If it is not present it will add a copy to the PREF_DIR
        and if it is different in structure (different section/options)
        it will merge the conf file with the new template one
    """
    active_conf = (PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve()
    template_conf = (BASE_DIR / 'config' / 'qtquickcontrols2.conf').resolve()

    if not active_conf.exists():
        copy_file(template_conf, active_conf)
    else:
        merge_config_files(active_conf, template_conf)


check_conf_file()
CONFIGURE_QT = Config((PREFERENCES_DIR / 'qtquickcontrols2.conf').resolve().as_posix())
