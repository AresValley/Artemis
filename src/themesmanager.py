from functools import partial
import os
import re
from PyQt5.QtWidgets import QAction, QActionGroup
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from constants import Constants, ThemeConstants
from utilities import pop_up


class _ColorsHandler:
    """Manage the theme's secondary colors.

    Contains a _Color inner class."""

    class _Color:
        """Characterize a color from a string.

        Can handle strings representing multiple colors."""

        _MAX_COLORS = 2

        def __init__(self, line):
            """Define the color from the string 'line'.

            All relevant features are defined:
            - if the format is valid;
            - if 'line' represent a single color or a list of colors.
            - the 'quality' of the color."""
            quality, color_str = line.split(ThemeConstants.COLOR_SEPARATOR)
            color_str = color_str.strip()
            self.quality = quality.lower().strip()
            self.color_str = ''
            self.color_list = []
            if ',' in color_str:
                self.is_simple_string = False
                self.color_list = [c.strip() for c in color_str.split(',')]
            else:
                self.is_simple_string = True
                self.color_str = color_str
            self.is_valid = self._color_is_valid()

        def _color_is_valid(self):
            """Return if the color (or the list of colors) has a valid html format."""
            pattern = "#([a-zA-Z0-9]){6}"

            def match_ok(col):
                return bool(re.match(pattern, col)) and len(col) == 7

            if not self.is_simple_string:
                if len(self.color_list) <= self._MAX_COLORS:
                    return all(match_ok(c) for c in self.color_list)
                else:
                    return False
            else:
                return match_ok(self.color_str)

    def __init__(self, simple_color_list, double_color_list):
        """Initialize the lists of valid _Color objects."""
        self.simple_color_list = simple_color_list
        self.double_color_list = double_color_list

    @classmethod
    def from_file(cls, colors_str):
        """Return a _ColorsHandler object with two lists of valid _Color objects.

        If the file is empty or there are no valid colors return None."""
        if colors_str:
            simple_color_list = []
            double_color_list = []
            for line in colors_str.splitlines():
                color = cls._Color(line)
                if color.is_valid:
                    if color.is_simple_string:
                        simple_color_list.append(color)
                    else:
                        double_color_list.append(color)
            if simple_color_list or double_color_list:
                return cls(simple_color_list, double_color_list)
        return None


class ThemeManager:
    """Manage all the operations releted to the themes."""

    def __init__(self, owner):
        """Initialize the ThemeManager instance."""
        self._owner = owner
        self._owner.active_color = ThemeConstants.DEFAULT_ACTIVE_COLOR
        self._owner.inactive_color = ThemeConstants.DEFAULT_INACTIVE_COLOR

        self._theme_path = ""
        self._current_theme = ""

        self._owner.spaceweather_screen.refreshable_labels.set(
            "switch_on_colors",
            ThemeConstants.DEFAULT_ON_COLORS
        )
        self._owner.spaceweather_screen.refreshable_labels.set(
            "switch_off_colors", ThemeConstants.DEFAULT_OFF_COLORS
        )
        self._theme_names = {}

    @pyqtSlot()
    def _apply(self, theme_path, save=True):
        """Apply the selected theme.

        Refresh all relevant widgets.
        Display a QMessageBox if the theme is not found."""
        self._theme_path = theme_path
        if os.path.exists(theme_path):
            if self._theme_path != self._current_theme:
                self._change(save)
                self._owner.display_specs(
                    item=self._owner.signals_list.currentItem(),
                    previous_item=None
                )
                self._owner.filters.refresh()
                self._owner.audio_widget.refresh(
                    self._owner.active_color,
                    self._owner.inactive_color
                )
                self._owner.spaceweather_screen.refreshable_labels.refresh()
        else:
            pop_up(self._owner, title=ThemeConstants.THEME_NOT_FOUND,
                   text=ThemeConstants.MISSING_THEME).show()

    def _pretty_name(self, bad_name):
        """Return a well-formatted theme name."""
        return ' '.join(
            map(
                lambda s: s.capitalize(),
                bad_name.split('_')
            )
        )

    def _detect_themes(self):
        """Detect all available themes.

        Connect all the actions to change the theme.
        Display a QMessageBox if the theme folder is not found."""
        themes = []
        ag = QActionGroup(self._owner, exclusive=True)
        themes_menu = self._owner.settings_menu.addMenu("Themes")
        if not os.path.exists(ThemeConstants.FOLDER):
            pop_up(self._owner, title=ThemeConstants.THEME_FOLDER_NOT_FOUND,
                   text=ThemeConstants.MISSING_THEME_FOLDER).show()
            return
        for theme_folder in sorted(os.listdir(ThemeConstants.FOLDER)):
            relative_folder = os.path.join(ThemeConstants.FOLDER, theme_folder)
            if os.path.isdir(os.path.abspath(relative_folder)):
                relative_folder = os.path.join(ThemeConstants.FOLDER, theme_folder)
                themes.append(relative_folder)
        for theme_path in themes:
            theme_name = '&' + self._pretty_name(os.path.basename(theme_path))
            new_theme = ag.addAction(
                QAction(
                    theme_name,
                    self._owner,
                    checkable=True
                )
            )
            themes_menu.addAction(new_theme)
            self._theme_names[theme_name.lstrip('&')] = new_theme
            new_theme.triggered.connect(partial(self._apply, theme_path))

    def _change(self, save=True):
        """Change the current theme.

        Apply the stylesheet and set active and inactive colors.
        Set all the new images needed.
        Save the new current theme on file."""
        theme_name = os.path.basename(self._theme_path) + ThemeConstants.EXTENSION
        try:
            with open(os.path.join(self._theme_path, theme_name), "r") as stylesheet:
                style = stylesheet.read()
            self._owner.setStyleSheet(style)
            self._owner.download_window.setStyleSheet(style)
        except FileNotFoundError:
            pop_up(self._owner, title=ThemeConstants.THEME_NOT_FOUND,
                   text=ThemeConstants.MISSING_THEME).show()
        else:
            icons_path = os.path.join(self._theme_path, ThemeConstants.ICONS_FOLDER)

            path_to_search_label = os.path.join(icons_path, Constants.SEARCH_LABEL_IMG)

            if os.path.exists(path_to_search_label):
                path = path_to_search_label
            else:
                path = ThemeConstants.DEFAULT_SEARCH_LABEL_PATH

            self._owner.search_label.setPixmap(QPixmap(path))
            self._owner.modulation_search_label.setPixmap(QPixmap(path))
            self._owner.location_search_label.setPixmap(QPixmap(path))

            self._owner.search_label.setScaledContents(True)
            self._owner.modulation_search_label.setScaledContents(True)
            self._owner.location_search_label.setScaledContents(True)

            path_to_volume_label = os.path.join(icons_path, Constants.VOLUME_LABEL_IMG)

            if os.path.exists(path_to_volume_label):
                path = path_to_volume_label
            else:
                path = ThemeConstants.DEFAULT_VOLUME_LABEL_PATH

            self._owner.volume_label.setPixmap(QPixmap(path))
            self._owner.volume_label.setScaledContents(True)

            path_to_colors = os.path.join(self._theme_path, ThemeConstants.COLORS)

            active_color_ok     = False
            inactive_color_ok   = False
            switch_on_color_ok  = False
            switch_off_color_ok = False
            text_color_ok       = False

            if os.path.exists(path_to_colors):
                with open(path_to_colors, "r") as colors_file:
                    color_handler = _ColorsHandler.from_file(colors_file.read())

                if color_handler is not None:
                    for color in color_handler.simple_color_list:
                        if color.quality == Constants.ACTIVE:
                            self._owner.active_color = color.color_str
                            active_color_ok = True
                        if color.quality == Constants.INACTIVE:
                            self._owner.inactive_color = color.color_str
                            inactive_color_ok = True
                        if color.quality == Constants.TEXT_COLOR:
                            text_color_ok = True
                            self._owner.spaceweather_screen.refreshable_labels.set(
                                "text_color",
                                color.color_str
                            )
                    for color in color_handler.double_color_list:
                        if color.quality == Constants.LABEL_ON_COLOR:
                            switch_on_color_ok = True
                            self._owner.spaceweather_screen.refreshable_labels.set(
                                "switch_on_colors",
                                color.color_list
                            )
                        if color.quality == Constants.LABEL_OFF_COLOR:
                            switch_off_color_ok = True
                            self._owner.spaceweather_screen.refreshable_labels.set(
                                "switch_off_colors",
                                color.color_list
                            )

            if not (active_color_ok and inactive_color_ok):
                self._owner.active_color = ThemeConstants.DEFAULT_ACTIVE_COLOR
                self._owner.inactive_color = ThemeConstants.DEFAULT_INACTIVE_COLOR

            if not (switch_on_color_ok and switch_off_color_ok):
                self._owner.spaceweather_screen.refreshable_labels.set(
                    "switch_on_colors",
                    ThemeConstants.DEFAULT_ON_COLORS
                )
                self._owner.spaceweather_screen.refreshable_labels.set(
                    "switch_off_colors",
                    ThemeConstants.DEFAULT_OFF_COLORS
                )

            if not text_color_ok:
                self._owner.spaceweather_screen.refreshable_labels.set(
                    "text_color",
                    ThemeConstants.DEFAULT_TEXT_COLOR
                )
            self._current_theme = self._theme_path
            if save:
                self._owner.settings.save(theme=os.path.basename(self._theme_path))

    def apply_default_theme(self):
        """Apply the default theme if no theme is set or the theme name is invalid."""
        try:
            self._theme_names[
                self._pretty_name(ThemeConstants.DEFAULT)
            ].setChecked(True)
        except Exception:
            pop_up(
                self._owner,
                title=ThemeConstants.THEME_NOT_FOUND,
                text=ThemeConstants.MISSING_THEME
            ).show()
        else:
            self._apply(ThemeConstants.DEFAULT_THEME_PATH)

    def start(self):
        """Start the theme manager."""
        self._detect_themes()
        if self._owner.settings.theme is not None:
            theme_path = os.path.join(ThemeConstants.FOLDER, self._owner.settings.theme)
            theme_name = self._pretty_name(os.path.basename(theme_path))
            try:
                self._theme_names[theme_name].setChecked(True)
            except Exception:
                self.apply_default_theme()
            else:
                self._apply(theme_path, save=False)
        else:
            self.apply_default_theme()
