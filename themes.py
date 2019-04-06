from functools import partial
import os
import re
from PyQt5.QtWidgets import QAction, QActionGroup
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from constants import Constants
from utilities import pop_up

class ThemeConstants(object):
    FOLDER                 = "themes"
    EXTENSION              = ".qss"
    ICONS_FOLDER           = "icons"
    DEFAULT                = "1-system"
    CURRENT                = ".current_theme"
    COLORS                 = "colors.txt"
    COLOR_SEPARATOR        = "="
    DEFAULT_ACTIVE_COLOR   = "#39eaff"
    DEFAULT_INACTIVE_COLOR = "#9f9f9f"
    THEME_NOT_FOUND        = "Theme not found"
    MISSING_THEME          = "Missing theme in '" + FOLDER + "' folder."

class Theme(object):
    def __init__(self, parent):
        self.__parent = parent
        self.__parent.active_color = ThemeConstants.DEFAULT_ACTIVE_COLOR
        self.__parent.inactive_color = ThemeConstants.DEFAULT_INACTIVE_COLOR
        self.__theme_path = ThemeConstants.DEFAULT
        self.__parent.default_images_folder = os.path.join(ThemeConstants.FOLDER,
                                                           ThemeConstants.DEFAULT,
                                                           ThemeConstants.ICONS_FOLDER)
        self.__theme_names = {}
        self.__detect_themes()

    def __refresh_range_labels(self):
        self.__parent.set_acf_interval_label()
        self.__parent.set_band_filter_label(self.__parent.activate_low_band_filter_btn,
                                            self.__parent.lower_band_spinbox,
                                            self.__parent.lower_band_filter_unit,
                                            self.__parent.lower_band_confidence,
                                            self.__parent.activate_up_band_filter_btn,
                                            self.__parent.upper_band_spinbox,
                                            self.__parent.upper_band_filter_unit,
                                            self.__parent.upper_band_confidence,
                                            self.__parent.band_range_lbl)
        self.__parent.set_band_filter_label(self.__parent.activate_low_freq_filter_btn,
                                            self.__parent.lower_freq_spinbox,
                                            self.__parent.lower_freq_filter_unit,
                                            self.__parent.lower_freq_confidence,
                                            self.__parent.activate_up_freq_filter_btn,
                                            self.__parent.upper_freq_spinbox,
                                            self.__parent.upper_freq_filter_unit,
                                            self.__parent.upper_freq_confidence,
                                            self.__parent.freq_range_lbl)

    @pyqtSlot()
    def __apply(self, theme_path):
        self.__theme_path = theme_path
        self.__change()
        self.__parent.display_specs(self.__parent.result_list.currentItem(), None)
        self.__refresh_range_labels()
        self.__parent.audio_widget.refresh_btns_colors(self.__parent.active_color, self.__parent.inactive_color)

    def __pretty_name(self, bad_name):
        return ' '.join(
            map(lambda s: s.capitalize(),
                bad_name.split('-')[1].split('_')
            )
        )

    def __detect_themes(self):
        themes = []
        ag = QActionGroup(self.__parent, exclusive = True)
        for theme_folder in os.listdir(ThemeConstants.FOLDER):
            relative_folder = os.path.join(ThemeConstants.FOLDER, theme_folder)
            if os.path.isdir(os.path.abspath(relative_folder)):
                relative_folder = os.path.join(ThemeConstants.FOLDER, theme_folder)
                themes.append(relative_folder)
        for theme_path in themes:
            theme_name = '&' + self.__pretty_name(os.path.basename(theme_path))
            new_theme = ag.addAction(QAction(theme_name, self.__parent, checkable = True))
            self.__parent.menu_themes.addAction(new_theme)
            self.__theme_names[theme_name.lstrip('&')] = new_theme
            new_theme.triggered.connect(partial(self.__apply, theme_path))

    def __change(self):
        try:
            with open(os.path.join(
                      self.__theme_path,
                      os.path.basename(self.__theme_path).split('-')[1] + ThemeConstants.EXTENSION), "r") as stylesheet:
                style = stylesheet.read()
                self.__parent.setStyleSheet(style)
                self.__parent.download_window.setStyleSheet(style)
        except FileNotFoundError:
            pop_up(self.__parent, title = ThemeConstants.THEME_NOT_FOUND,
                   text = ThemeConstants.MISSING_THEME).show()
        else:
            icons_path = os.path.join(self.__theme_path, ThemeConstants.ICONS_FOLDER)
            default_icons_path = os.path.join(ThemeConstants.FOLDER,
                                              ThemeConstants.DEFAULT,
                                              ThemeConstants.ICONS_FOLDER)

            if os.path.exists(os.path.join(icons_path, Constants.NOT_SELECTED)) and \
               os.path.exists(os.path.join(icons_path, Constants.NOT_AVAILABLE)):
                self.__parent.default_images_folder = icons_path
            else:
                self.__parent.default_images_folder = default_icons_path

            path_to_search_label = os.path.join(icons_path, Constants.SEARCH_LABEL_IMG)
            default_search_label = os.path.join(default_icons_path, Constants.SEARCH_LABEL_IMG)

            if os.path.exists(path_to_search_label):
                self.__parent.search_label.setPixmap(QPixmap(path_to_search_label))
                self.__parent.modulation_search_label.setPixmap(QPixmap(path_to_search_label))
                self.__parent.location_search_label.setPixmap(QPixmap(path_to_search_label))
            else:
                self.__parent.search_label.setPixmap(QPixmap(default_search_label))
                self.__parent.modulation_search_label.setPixmap(QPixmap(default_search_label))
                self.__parent.location_search_label.setPixmap(QPixmap(default_search_label))

            self.__parent.search_label.setScaledContents(True)
            self.__parent.modulation_search_label.setScaledContents(True)
            self.__parent.location_search_label.setScaledContents(True)

            path_to_volume_label = os.path.join(icons_path, Constants.VOLUME_LABEL_IMG)
            default_volume_label = os.path.join(default_icons_path, Constants.VOLUME_LABEL_IMG)

            if os.path.exists(path_to_volume_label):
                self.__parent.volume_label.setPixmap(QPixmap(path_to_volume_label))
            else:
                self.__parent.volume_label.setPixmap(QPixmap(default_volume_label))

            self.__parent.volume_label.setScaledContents(True)

            path_to_colors = os.path.join(self.__theme_path, ThemeConstants.COLORS)
            active_color_ok = False
            inactive_color_ok = False
            valid_format = False
            valid_file = False
            if os.path.exists(path_to_colors):
                valid_file = True
                with open(path_to_colors, "r") as colors_file:
                    for line in colors_file:
                        if ThemeConstants.COLOR_SEPARATOR in line:
                            valid_format = True
                            quality, color = line.split(ThemeConstants.COLOR_SEPARATOR)
                            color = color.rstrip()
                            is_valid_html_color = lambda color : bool(re.match("#([a-zA-Z0-9]){6}", color))
                            if quality.lower() == Constants.ACTIVE and is_valid_html_color(color):
                                self.__parent.active_color = color
                                active_color_ok = True
                            if quality.lower() == Constants.INACTIVE and is_valid_html_color(color):
                                self.__parent.inactive_color = color
                                inactive_color_ok = True

            if not all([valid_file, valid_format, active_color_ok, inactive_color_ok]):
                self.__parent.active_color = ThemeConstants.DEFAULT_ACTIVE_COLOR
                self.__parent.inactive_color = ThemeConstants.DEFAULT_INACTIVE_COLOR

            try:
                with open(os.path.join(ThemeConstants.FOLDER,
                          ThemeConstants.CURRENT), "w") as current_theme:
                    current_theme.write(self.__theme_path)
            except:
                pass

    def initialize(self):
        current_theme_file = os.path.join(ThemeConstants.FOLDER, ThemeConstants.CURRENT)
        if os.path.exists(current_theme_file):
            with open(current_theme_file, "r") as current_theme_path:
                theme_path = current_theme_path.read()
                theme_name = self.__pretty_name(os.path.basename(theme_path))
                self.__theme_names[theme_name].setChecked(True)
                if theme_path != ThemeConstants.DEFAULT:
                    self.__apply(theme_path)
        else:
            self.__theme_names[self.__pretty_name(ThemeConstants.DEFAULT)].setChecked(True)
