from collections import namedtuple
from functools import partial
import webbrowser
import os
import sys
from time import sleep, time

from pandas import read_csv

from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             qApp,
                             QDesktopWidget,
                             QListWidgetItem,
                             QMessageBox,
                             QSplashScreen,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import (QFileInfo,
                          Qt,
                          pyqtSlot,)
from acfvalue import ACFValue
from audio_player import AudioPlayer
from weatherdata import ForecastData
from download_window import DownloadWindow
from spaceweathermanager import SpaceWeatherManager
from constants import (Constants,
                       GfdType,
                       Database,
                       ChecksumWhat,
                       Messages,
                       Signal,)
from themesmanager import ThemeManager
from filters import Filters
from utilities import (checksum_ok,
                       pop_up,
                       is_undef_freq,
                       is_undef_band,
                       format_numbers,
                       resource_path,
                       safe_cast,
                       is_mac_os)

# import default_imgs_rc

__VERSION__ = "3.0.1"
qt_creator_file = resource_path("artemis.ui")
Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)


class Artemis(QMainWindow, Ui_MainWindow):
    """Main application class."""

    def __init__(self):
        """Set all connections of the application."""
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ARTΣMIS " + __VERSION__)
        self.set_initial_size()
        self.closing = False
        self.download_window = DownloadWindow()
        self.download_window.complete.connect(self.show_downloaded_signals)
        self.actionExit.triggered.connect(qApp.quit)
        self.action_update_database.triggered.connect(self.ask_if_download)
        self.action_check_db_ver.triggered.connect(self.check_db_ver)
        self.action_sigidwiki_com.triggered.connect(
            lambda: webbrowser.open(Constants.SIGIDWIKI)
        )
        self.action_add_a_signal.triggered.connect(
            lambda: webbrowser.open(Constants.ADD_SIGNAL_LINK)
        )
        self.action_aresvalley_com.triggered.connect(
            lambda: webbrowser.open(Constants.ARESVALLEY_LINK)
        )
        self.action_forum.triggered.connect(
            lambda: webbrowser.open(Constants.FORUM_LINK)
        )
        self.action_rtl_sdr_com.triggered.connect(
            lambda: webbrowser.open(Constants.RTL_SDL_LINK)
        )
        self.db = None
        self.current_signal_name = ''
        self.signal_names = []
        self.total_signals = 0

        # Forecast
        self.forecast_info_btn.clicked.connect(
            lambda: webbrowser.open(Constants.SPACE_WEATHER_INFO)
        )
        self.forecast_data = ForecastData(self)
        self.update_forecast_bar.clicked.connect(self.start_update_forecast)
        self.update_forecast_bar.set_idle()
        self.forecast_data.update_complete.connect(self.update_forecast)

        # Spaceweather manager
        self.spaceweather_screen = SpaceWeatherManager(self)

        self.theme_manager = ThemeManager(self)

        self.filters = Filters(self)

# #######################################################################################

        UrlColors = namedtuple("UrlColors", ["inactive", "active", "clicked"])
        self.url_button.colors = UrlColors("#9f9f9f", "#4c75ff", "#942ccc")
        self.category_labels = [
            self.cat_mil,
            self.cat_rad,
            self.cat_active,
            self.cat_inactive,
            self.cat_ham,
            self.cat_comm,
            self.cat_avi,
            self.cat_mar,
            self.cat_ana,
            self.cat_dig,
            self.cat_trunked,
            self.cat_utility,
            self.cat_sat,
            self.cat_navi,
            self.cat_interf,
            self.cat_num_stat,
            self.cat_time_sig
        ]

        self.property_labels = [
            self.freq_lab,
            self.band_lab,
            self.mode_lab,
            self.modul_lab,
            self.loc_lab,
            self.acf_lab,
            self.description_text
        ]

        self.url_button.clicked.connect(self.go_to_web_page_signal)

        # GFD
        self.freq_search_gfd_btn.clicked.connect(partial(self.go_to_gfd, GfdType.FREQ))
        self.location_search_gfd_btn.clicked.connect(partial(self.go_to_gfd, GfdType.LOC))
        self.gfd_line_edit.returnPressed.connect(partial(self.go_to_gfd, GfdType.LOC))

# ##########################################################################################

        # Left list widget and search bar.
        self.search_bar.textChanged.connect(self.display_signals)
        self.signals_list.currentItemChanged.connect(self.display_specs)
        self.signals_list.itemDoubleClicked.connect(self.set_visible_tab)

        self.audio_widget = AudioPlayer(
            self.play,
            self.pause,
            self.stop,
            self.volume,
            self.loop,
            self.audio_progress,
            self.active_color,
            self.inactive_color
        )

        BandLabel = namedtuple("BandLabel", ["left", "center", "right"])
        self.band_labels = [
            BandLabel(self.elf_left, self.elf, self.elf_right),
            BandLabel(self.slf_left, self.slf, self.slf_right),
            BandLabel(self.ulf_left, self.ulf, self.ulf_right),
            BandLabel(self.vlf_left, self.vlf, self.vlf_right),
            BandLabel(self.lf_left, self.lf, self.lf_right),
            BandLabel(self.mf_left, self.mf, self.mf_right),
            BandLabel(self.hf_left, self.hf, self.hf_right),
            BandLabel(self.vhf_left, self.vhf, self.vhf_right),
            BandLabel(self.uhf_left, self.uhf, self.uhf_right),
            BandLabel(self.shf_left, self.shf, self.shf_right),
            BandLabel(self.ehf_left, self.ehf, self.ehf_right),
        ]

        self.main_tab.currentChanged.connect(self.hide_show_right_widget)

# Final operations.
        self.theme_manager.start()
        self.load_db()
        self.display_signals()

    @pyqtSlot()
    def hide_show_right_widget(self):
        if self.main_tab.currentWidget() == self.forecast_tab:
            self.fixed_audio_and_image.setVisible(False)
        elif not self.fixed_audio_and_image.isVisible():
            self.fixed_audio_and_image.setVisible(True)

    @pyqtSlot()
    def set_visible_tab(self):
        """Set the current main tab when double-clicking a signal name.

        Switch between main and filter tab when double-clicking multiple times."""
        set_main = False
        if self.main_tab.currentWidget() != self.signal_properties_tab:
            self.main_tab.setCurrentWidget(self.signal_properties_tab)
            set_main = True
        if self.signal_tab.currentWidget() != self.signal_main_tab or set_main:
            self.signal_tab.setCurrentWidget(self.signal_main_tab)
        else:
            self.signal_tab.setCurrentWidget(self.filter_tab)

    @pyqtSlot()
    def start_update_forecast(self):
        """Start the update of the 3-day forecast screen.

        Start the corresponding thread.
        """
        if not self.forecast_data.is_updating:
            self.update_forecast_bar.set_updating()
            self.forecast_data.update()

    @pyqtSlot(bool)
    def update_forecast(self, status_ok):
        """Update the 3-day forecast screen after a successful download.

        If the download was not successful throw a warning. In any case remove
        the downloaded data.
        """
        self.update_forecast_bar.set_idle()
        if status_ok:
            self.forecast_data.update_all_labels()
        elif not self.closing:
            pop_up(self, title=Messages.BAD_DOWNLOAD,
                   text=Messages.BAD_DOWNLOAD_MSG).show()
        self.forecast_data.remove_data()

    @pyqtSlot()
    def go_to_gfd(self, by):
        """Open a browser tab with the GFD site.

        Make the search by frequency or location.
        Argument:
        by -- either GfdType.FREQ or GfdType.LOC.
        """
        query = "/?q="
        if by is GfdType.FREQ:
            value_in_mhz = self.freq_gfd.value() \
                * Constants.CONVERSION_FACTORS[self.unit_freq_gfd.currentText()] \
                / Constants.CONVERSION_FACTORS["MHz"]
            query += str(value_in_mhz)
        elif by is GfdType.LOC:
            query += self.gfd_line_edit.text()
        try:
            webbrowser.open(Constants.GFD_SITE + query.lower())
        except Exception:
            pass

    def set_initial_size(self):
        """Handle high resolution screens.

        Set bigger sizes for all the relevant fixed-size widgets.
        """
        d = QDesktopWidget().availableGeometry()
        w = d.width()
        h = d.height()
        self.showMaximized()

        if w > 3000 or h > 2000:
            self.fixed_audio_and_image.setFixedSize(540, 1150)
            self.fixed_audio_and_image.setMaximumSize(540, 1150)
            audio_btn_h, audio_btn_w = 90, 90
            self.play.setFixedSize(audio_btn_h, audio_btn_w)
            self.pause.setFixedSize(audio_btn_h, audio_btn_w)
            self.stop.setFixedSize(audio_btn_h, audio_btn_w)
            self.loop.setFixedSize(audio_btn_h, audio_btn_w)
            self.lower_freq_spinbox.setFixedWidth(200)
            self.upper_freq_spinbox.setFixedWidth(200)
            self.lower_freq_filter_unit.setFixedWidth(120)
            self.upper_freq_filter_unit.setFixedWidth(120)
            self.lower_freq_confidence.setFixedWidth(120)
            self.upper_freq_confidence.setFixedWidth(120)

            self.lower_band_spinbox.setFixedWidth(200)
            self.upper_band_spinbox.setFixedWidth(200)
            self.lower_band_filter_unit.setFixedWidth(120)
            self.upper_band_filter_unit.setFixedWidth(120)
            self.lower_band_confidence.setFixedWidth(120)
            self.upper_band_confidence.setFixedWidth(120)

            self.freq_gfd.setFixedWidth(200)
            self.unit_freq_gfd.setFixedWidth(120)

            self.mode_tree_widget.setMinimumWidth(500)
            self.modulation_list.setMinimumWidth(500)
            self.locations_list.setMinimumWidth(500)

            self.audio_progress.setFixedHeight(20)
            self.volume.setStyleSheet("""
                QSlider::groove:horizontal {
                    height: 12px;
                    background: #7a7a7a;
                    margin: 0 10px;
                    border-radius: 6px
                }
                QSlider::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 gray, stop:0.5 white, stop:1.0 gray);
                    border: 1px solid #5c5c5c;
                    width: 28px;
                    margin: -8px -8px;
                    border-radius: 14px;
                }
                """)

    @pyqtSlot()
    def download_db(self):
        """Start the database download.

        Do nothing if already downloading.
        """
        if not self.download_window.isVisible():
            self.download_window.start_download()
            self.download_window.show()

    @pyqtSlot()
    def ask_if_download(self):
        """Check if the database is at its latest version.

        If a new database is available automatically start the download.
        If not ask if should download it anyway.
        If already downloading do nothing.
        Handle possible connection errors.
        """
        if not self.download_window.isVisible():
            db_path = os.path.join(Constants.DATA_FOLDER, Database.NAME)
            try:
                with open(db_path, "rb") as file_db:
                    db = file_db.read()
            except Exception:
                self.download_db()
            else:
                try:
                    is_checksum_ok = checksum_ok(db, ChecksumWhat.DB)
                except Exception:
                    pop_up(self, title=Messages.NO_CONNECTION,
                           text=Messages.NO_CONNECTION_MSG).show()
                else:
                    if not is_checksum_ok:
                        self.download_db()
                    else:
                        answer = pop_up(self, title=Messages.DB_UP_TO_DATE,
                                        text=Messages.DB_UP_TO_DATE_MSG,
                                        informative_text=Messages.DOWNLOAD_ANYWAY_QUESTION,
                                        is_question=True,
                                        default_btn=QMessageBox.No).exec()
                        if answer == QMessageBox.Yes:
                            self.download_db()

    @pyqtSlot()
    def check_db_ver(self):
        """Check if the database is at its latest version.

        If a new database version is available, ask if it should be downloaded.
        If a new database version is not available display a message.
        If already downloading do nothing.
        Handle possible connection errors.
        """
        if not self.download_window.isVisible():
            db_path = os.path.join(Constants.DATA_FOLDER, Database.NAME)
            answer = None
            try:
                with open(db_path, "rb") as file_db:
                    db = file_db.read()
            except Exception:
                answer = pop_up(self, title=Messages.NO_DB,
                                text=Messages.NO_DB_AVAIL,
                                informative_text=Messages.DOWNLOAD_NOW_QUESTION,
                                is_question=True).exec()
                if answer == QMessageBox.Yes:
                    self.download_db()
            else:
                try:
                    is_checksum_ok = checksum_ok(db, ChecksumWhat.DB)
                except Exception:
                    pop_up(self, title=Messages.NO_CONNECTION,
                           text=Messages.NO_CONNECTION_MSG).show()
                else:
                    if is_checksum_ok:
                        pop_up(self, title=Messages.DB_UP_TO_DATE,
                               text=Messages.DB_UP_TO_DATE_MSG).show()
                    else:
                        answer = pop_up(self, title=Messages.DB_NEW_VER,
                                        text=Messages.DB_NEW_VER_MSG,
                                        informative_text=Messages.DOWNLOAD_NOW_QUESTION,
                                        is_question=True).exec()
                        if answer == QMessageBox.Yes:
                            self.download_db()

    @pyqtSlot()
    def show_downloaded_signals(self):
        """Load and display the database signal list."""
        self.search_bar.setEnabled(True)
        self.load_db()
        self.display_signals()

    def load_db(self):
        """Load the database from file.

        Populate the signals list and set the total number of signals.
        Handle possible missing file error.
        """
        try:
            self.db = read_csv(os.path.join(Constants.DATA_FOLDER, Database.NAME),
                               sep=Database.DELIMITER,
                               header=None,
                               index_col=0,
                               dtype={name: str for name in Database.STRINGS},
                               names=Database.NAMES)
        except FileNotFoundError:
            self.search_bar.setDisabled(True)
            answer = pop_up(self, title=Messages.NO_DB,
                            text=Messages.NO_DB_AVAIL,
                            informative_text=Messages.DOWNLOAD_NOW_QUESTION,
                            is_question=True).exec()
            if answer == QMessageBox.Yes:
                self.download_db()
        else:
            # Avoid a crash if there are duplicated signals
            self.db = self.db.groupby(level=0).first()
            self.signal_names = self.db.index
            self.total_signals = len(self.signal_names)
            self.db.fillna(Constants.UNKNOWN, inplace=True)
            self.db[Signal.ACF] = ACFValue.list_from_series(self.db[Signal.ACF])
            self.db[Signal.WIKI_CLICKED] = False
            self.update_status_tip(self.total_signals)
            self.signals_list.clear()
            self.signals_list.addItems(self.signal_names)
            self.signals_list.setCurrentItem(None)
            self.modulation_list.addItems(
                self.collect_list(
                    Signal.MODULATION
                )
            )
            self.locations_list.addItems(
                self.collect_list(
                    Signal.LOCATION
                )
            )

    def collect_list(self, list_property, separator=Constants.FIELD_SEPARATOR):
        """Collect all the entrys of a QListWidget.

        Handle multiple entries in one item seprated by a separator.
        Keyword argument:
        separator -- the separator character for multiple-entries items.
        """
        values = self.db[list_property]
        values = list(
            set([
                x.strip() for value in values[values != Constants.UNKNOWN]
                for x in value.split(separator)
            ])
        )
        values.sort()
        values.insert(0, Constants.UNKNOWN)
        return values

    @pyqtSlot()
    def activate_if_toggled(self, radio_btn, *widgets):
        """If radio_btn is toggled, activate all *widgets.

        Do nothing otherwise.
        """
        toggled = radio_btn.isChecked()
        for w in widgets[:-1]:  # Neglect the bool coming from the emitted signal.
            w.setEnabled(toggled)

    @pyqtSlot()
    def display_signals(self):
        """Display all the signal names which matches the applied filters."""
        text = self.search_bar.text()
        available_signals = 0
        for index, signal_name in enumerate(self.signal_names):
            if text.lower() in signal_name.lower() and self.filters.ok(signal_name):
                self.signals_list.item(index).setHidden(False)
                available_signals += 1
            else:
                self.signals_list.item(index).setHidden(True)
        # Remove selected item.
        self.signals_list.setCurrentItem(None)
        self.update_status_tip(available_signals)

    def update_status_tip(self, available_signals):
        """Display the number of displayed signals in the status tip."""
        if available_signals < self.total_signals:
            self.statusbar.setStyleSheet(f'color: {self.active_color}')
        else:
            self.statusbar.setStyleSheet(f'color: {self.inactive_color}')
        self.statusbar.showMessage(
            f"{available_signals} out of {self.total_signals} signals displayed."
        )

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def display_specs(self, item, previous_item):
        """Display the signal properties.

        'item' is the item corresponding to the selected signal
        'previous_item' is unused.
        """
        self.display_spectrogram()
        if item is not None:
            self.current_signal_name = item.text()
            self.name_lab.setText(self.current_signal_name)
            self.name_lab.setAlignment(Qt.AlignHCenter)
            current_signal = self.db.loc[self.current_signal_name]
            self.url_button.setEnabled(True)
            if not current_signal.at[Signal.WIKI_CLICKED]:
                self.url_button.setStyleSheet(
                    f"color: {self.url_button.colors.active};"
                )
            else:
                self.url_button.setStyleSheet(
                    f"color: {self.url_button.colors.clicked};"
                )
            category_code = current_signal.at[Signal.CATEGORY_CODE]
            undef_freq = is_undef_freq(current_signal)
            undef_band = is_undef_band(current_signal)
            if not undef_freq:
                self.freq_lab.setText(
                    format_numbers(
                        current_signal.at[Signal.INF_FREQ],
                        current_signal.at[Signal.SUP_FREQ]
                    )
                )
            else:
                self.freq_lab.setText("Undefined")
            if not undef_band:
                self.band_lab.setText(
                    format_numbers(
                        current_signal.at[Signal.INF_BAND],
                        current_signal.at[Signal.SUP_BAND]
                    )
                )
            else:
                self.band_lab.setText("Undefined")

            self.mode_lab.setText(current_signal.at[Signal.MODE])
            self.modul_lab.setText(current_signal.at[Signal.MODULATION])
            self.loc_lab.setText(current_signal.at[Signal.LOCATION])
            self.acf_lab.setText(
                ACFValue.concat_strings(current_signal.at[Signal.ACF])
            )
            self.description_text.setText(current_signal.at[Signal.DESCRIPTION])
            for cat, cat_lab in zip(category_code, self.category_labels):
                if cat == '0':
                    cat_lab.setStyleSheet(f"color: {self.inactive_color};")
                elif cat == '1':
                    cat_lab.setStyleSheet(f"color: {self.active_color};")
            self.set_band_range(current_signal)
            self.audio_widget.set_audio_player(self.current_signal_name)
        else:
            self.url_button.setEnabled(False)
            self.url_button.setStyleSheet(
                f"color: {self.url_button.colors.inactive};"
            )
            self.current_signal_name = ''
            self.name_lab.setText("No Signal")
            self.name_lab.setAlignment(Qt.AlignHCenter)
            for lab in self.property_labels:
                lab.setText(Constants.UNKNOWN)
            for lab in self.category_labels:
                lab.setStyleSheet(f"color: {self.inactive_color};")
            self.set_band_range()
            self.audio_widget.set_audio_player()

    def display_spectrogram(self):
        """Display the selected signal's waterfall."""
        default_pic = Constants.DEFAULT_NOT_SELECTED
        item = self.signals_list.currentItem()
        if item:
            spectrogram_name = item.text()
            path_spectr = os.path.join(
                Constants.DATA_FOLDER,
                Constants.SPECTRA_FOLDER,
                spectrogram_name + Constants.SPECTRA_EXT
            )
            if not QFileInfo(path_spectr).exists():
                path_spectr = Constants.DEFAULT_NOT_AVAILABLE
        else:
            path_spectr = default_pic
        self.spectrogram.setPixmap(QPixmap(path_spectr))

    def activate_band_category(self, band_label, activate=True):
        """Highlight the given band_label.

        If activate is False remove the highlight (default to True).
        """
        color = self.active_color if activate else self.inactive_color
        for label in band_label:
            label.setStyleSheet(f"color: {color};")

    def set_band_range(self, current_signal=None):
        """Highlight the signal's band labels.

        If no signal is selected remove all highlights.
        """
        if current_signal is not None and not is_undef_freq(current_signal):
            lower_freq = safe_cast(
                current_signal.at[Signal.INF_FREQ], int
            )
            upper_freq = safe_cast(
                current_signal.at[Signal.SUP_FREQ], int
            )
            zipped = list(zip(Constants.BANDS, self.band_labels))
            for i, w in enumerate(zipped):
                band, band_label = w
                if lower_freq >= band.lower and lower_freq < band.upper:
                    self.activate_band_category(band_label)
                    for uband, uband_label in zipped[i + 1:]:
                        if upper_freq > uband.lower:
                            self.activate_band_category(uband_label)
                        else:
                            self.activate_band_category(uband_label, False)
                    break
                else:
                    self.activate_band_category(band_label, False)
        else:
            for band_label in self.band_labels:
                self.activate_band_category(band_label, False)

    @pyqtSlot()
    def go_to_web_page_signal(self):
        """Go the web page of the signal's wiki.

        Do nothing if no signal is selected.
        """
        if self.current_signal_name:
            self.url_button.setStyleSheet(
                f"color: {self.url_button.colors.clicked}"
            )
            webbrowser.open(self.db.at[self.current_signal_name, Signal.URL])
            self.db.at[self.current_signal_name, Signal.WIKI_CLICKED] = True

    def closeEvent(self, event):
        """Extends closeEvent of QMainWindow.

        Shutdown all active threads and close all open windows."""
        self.closing = True
        if self.download_window.isVisible():
            self.download_window.close()
        if self.space_weather_data.is_updating:
            self.space_weather_data.shutdown_thread()
        if self.forecast_data.is_updating:
            self.forecast_data.shutdown_thread()
        super().closeEvent(event)


if __name__ == '__main__':
    # For executables running on Mac Os systems.
    if hasattr(sys, "_MEIPASS") and is_mac_os():
        os.chdir(sys._MEIPASS)

    my_app = QApplication(sys.argv)
    ARTEMIS_ICON = os.path.join(":", "icon", "default_pics", "Artemis3.500px.png")
    img = QPixmap(ARTEMIS_ICON)
    splash = QSplashScreen(img)
    splash.show()
    start = time()
    while time() - start < 1.5:
        sleep(0.001)
        my_app.processEvents()
    splash.close()
    artemis = Artemis()
    artemis.show()
    sys.exit(my_app.exec_())
