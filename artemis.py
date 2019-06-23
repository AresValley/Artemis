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
                             QSplashScreen,
                             QTreeWidgetItem,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import (QFileInfo,
                          Qt,
                          pyqtSlot,
                          QRect,)

from audio_player import AudioPlayer
from weatherdata import SpaceWeatherData, ForecastData
from download_window import DownloadWindow
from switchable_label import SwitchableLabelsIterable
from constants import (Constants,
                       Ftype,
                       GfdType,
                       Database,
                       ChecksumWhat,
                       Messages,
                       Signal,)
from themesmanager import ThemeManager
from utilities import (checksum_ok,
                       uncheck_and_emit,
                       pop_up,
                       connect_events_to_func,
                       filters_limit,
                       is_undef_freq,
                       is_undef_band,
                       format_numbers,
                       resource_path,
                       safe_cast)

# import default_imgs_rc


qt_creator_file = resource_path("artemis.ui")
Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)


class Artemis(QMainWindow, Ui_MainWindow):
    """Main application class."""

    def __init__(self):
        """Set all connections of the application."""
        super().__init__()
        self.setupUi(self)
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

        self.switchable_r_labels = SwitchableLabelsIterable(
            self.r0_now_lbl,
            self.r1_now_lbl,
            self.r2_now_lbl,
            self.r3_now_lbl,
            self.r4_now_lbl,
            self.r5_now_lbl
        )

        self.switchable_s_labels = SwitchableLabelsIterable(
            self.s0_now_lbl,
            self.s1_now_lbl,
            self.s2_now_lbl,
            self.s3_now_lbl,
            self.s4_now_lbl,
            self.s5_now_lbl
        )

        self.switchable_g_now_labels = SwitchableLabelsIterable(
            self.g0_now_lbl,
            self.g1_now_lbl,
            self.g2_now_lbl,
            self.g3_now_lbl,
            self.g4_now_lbl,
            self.g5_now_lbl
        )

        self.switchable_g_today_labels = SwitchableLabelsIterable(
            self.g0_today_lbl,
            self.g1_today_lbl,
            self.g2_today_lbl,
            self.g3_today_lbl,
            self.g4_today_lbl,
            self.g5_today_lbl
        )

        self.k_storm_labels = SwitchableLabelsIterable(
            self.k_ex_sev_storm_lbl,
            self.k_very_sev_storm_lbl,
            self.k_sev_storm_lbl,
            self.k_maj_storm_lbl,
            self.k_min_storm_lbl,
            self.k_active_lbl,
            self.k_unsettled_lbl,
            self.k_quiet_lbl,
            self.k_very_quiet_lbl,
            self.k_inactive_lbl
        )

        self.a_storm_labels = SwitchableLabelsIterable(
            self.a_sev_storm_lbl,
            self.a_maj_storm_lbl,
            self.a_min_storm_lbl,
            self.a_active_lbl,
            self.a_unsettled_lbl,
            self.a_quiet_lbl
        )

        self.space_weather_labels = (
            self.space_weather_lbl_0,
            self.space_weather_lbl_1,
            self.space_weather_lbl_2,
            self.space_weather_lbl_3,
            self.space_weather_lbl_4,
            self.space_weather_lbl_5,
            self.space_weather_lbl_6,
            self.space_weather_lbl_7,
            self.space_weather_lbl_8
        )

        for lab in self.space_weather_labels:
            lab.set_default_stylesheet()

        self.space_weather_label_container.labels = self.space_weather_labels
        self.space_weather_label_name_container.labels = [
            self.eme_lbl,
            self.ms_lbl,
            self.muf_lbl,
            self.hi_lbl,
            self.eu50_lbl,
            self.eu70_lbl,
            self.eu144_lbl,
            self.na_lbl,
            self.aurora_lbl
        ]
        self.theme_manager = ThemeManager(self)

        # Manage frequency filters.
        self.frequency_filters_btns = (
            self.elf_filter_btn,
            self.slf_filter_btn,
            self.ulf_filter_btn,
            self.vlf_filter_btn,
            self.lf_filter_btn,
            self.mf_filter_btn,
            self.hf_filter_btn,
            self.vhf_filter_btn,
            self.uhf_filter_btn,
            self.shf_filter_btn,
            self.ehf_filter_btn,
        )

        connect_events_to_func(
            events_to_connect=[self.lower_freq_spinbox.valueChanged,
                               self.upper_freq_spinbox.valueChanged,
                               self.lower_freq_filter_unit.currentTextChanged,
                               self.upper_freq_filter_unit.currentTextChanged,
                               self.activate_low_freq_filter_btn.toggled],
            fun_to_connect=self.set_min_value_upper_limit,
            fun_args=[self.lower_freq_filter_unit,
                      self.lower_freq_spinbox,
                      self.upper_freq_filter_unit,
                      self.upper_freq_spinbox]
        )

        connect_events_to_func(
            events_to_connect=[self.lower_freq_spinbox.valueChanged,
                               self.upper_freq_spinbox.valueChanged,
                               self.lower_freq_filter_unit.currentTextChanged,
                               self.upper_freq_filter_unit.currentTextChanged,
                               self.activate_low_freq_filter_btn.clicked,
                               self.activate_up_freq_filter_btn.clicked,
                               self.lower_freq_confidence.valueChanged,
                               self.upper_freq_confidence.valueChanged],
            fun_to_connect=self.set_band_filter_label,
            fun_args=[self.activate_low_freq_filter_btn,
                      self.lower_freq_spinbox,
                      self.lower_freq_filter_unit,
                      self.lower_freq_confidence,
                      self.activate_up_freq_filter_btn,
                      self.upper_freq_spinbox,
                      self.upper_freq_filter_unit,
                      self.upper_freq_confidence,
                      self.freq_range_lbl]
        )

        self.activate_low_freq_filter_btn.toggled.connect(
            partial(self.activate_if_toggled,
                    self.activate_low_freq_filter_btn,
                    self.lower_freq_spinbox,
                    self.lower_freq_filter_unit,
                    self.lower_freq_confidence)
        )

        self.activate_up_freq_filter_btn.toggled.connect(
            partial(self.activate_if_toggled,
                    self.activate_up_freq_filter_btn,
                    self.upper_freq_spinbox,
                    self.upper_freq_filter_unit,
                    self.upper_freq_confidence)
        )

        self.apply_remove_freq_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_freq_filter_btn.set_slave_filters(
            simple_ones=[
                *self.frequency_filters_btns,
                self.include_undef_freqs,
                self.activate_low_freq_filter_btn,
                self.activate_up_freq_filter_btn
            ],
            radio_1=self.activate_low_freq_filter_btn,
            ruled_by_radio_1=[
                self.lower_freq_spinbox,
                self.lower_freq_filter_unit,
                self.lower_freq_confidence
            ],
            radio_2=self.activate_up_freq_filter_btn,
            ruled_by_radio_2=[
                self.upper_freq_spinbox,
                self.upper_freq_filter_unit,
                self.upper_freq_confidence
            ]
        )
        self.apply_remove_freq_filter_btn.clicked.connect(self.display_signals)
        self.reset_frequency_filters_btn.clicked.connect(
            partial(self.reset_fb_filters, Ftype.FREQ)
        )

        # Manage bandwidth filters.

        connect_events_to_func(
            events_to_connect=[self.lower_band_spinbox.valueChanged,
                               self.upper_band_spinbox.valueChanged,
                               self.lower_band_filter_unit.currentTextChanged,
                               self.upper_band_filter_unit.currentTextChanged,
                               self.activate_low_band_filter_btn.toggled],
            fun_to_connect=self.set_min_value_upper_limit,
            fun_args=[self.lower_band_filter_unit,
                      self.lower_band_spinbox,
                      self.upper_band_filter_unit,
                      self.upper_band_spinbox]
        )

        connect_events_to_func(
            events_to_connect=[self.lower_band_spinbox.valueChanged,
                               self.upper_band_spinbox.valueChanged,
                               self.lower_band_filter_unit.currentTextChanged,
                               self.upper_band_filter_unit.currentTextChanged,
                               self.activate_low_band_filter_btn.clicked,
                               self.activate_up_band_filter_btn.clicked,
                               self.lower_band_confidence.valueChanged,
                               self.upper_band_confidence.valueChanged],
            fun_to_connect=self.set_band_filter_label,
            fun_args=[self.activate_low_band_filter_btn,
                      self.lower_band_spinbox,
                      self.lower_band_filter_unit,
                      self.lower_band_confidence,
                      self.activate_up_band_filter_btn,
                      self.upper_band_spinbox,
                      self.upper_band_filter_unit,
                      self.upper_band_confidence,
                      self.band_range_lbl]
        )

        self.activate_low_band_filter_btn.toggled.connect(
            partial(self.activate_if_toggled,
                    self.activate_low_band_filter_btn,
                    self.lower_band_spinbox,
                    self.lower_band_filter_unit,
                    self.lower_band_confidence)
        )

        self.activate_up_band_filter_btn.toggled.connect(
            partial(self.activate_if_toggled,
                    self.activate_up_band_filter_btn,
                    self.upper_band_spinbox,
                    self.upper_band_filter_unit,
                    self.upper_band_confidence)
        )

        self.apply_remove_band_filter_btn.set_texts(Constants.APPLY,
                                                    Constants.REMOVE)
        self.apply_remove_band_filter_btn.set_slave_filters(
            simple_ones=[
                self.include_undef_bands,
                self.activate_low_band_filter_btn,
                self.activate_up_band_filter_btn
            ],
            radio_1=self.activate_low_band_filter_btn,
            ruled_by_radio_1=[
                self.lower_band_spinbox,
                self.lower_band_filter_unit,
                self.lower_band_confidence
            ],
            radio_2=self.activate_up_band_filter_btn,
            ruled_by_radio_2=[
                self.upper_band_spinbox,
                self.upper_band_filter_unit,
                self.upper_band_confidence
            ]
        )
        self.apply_remove_band_filter_btn.clicked.connect(self.display_signals)
        self.reset_band_filters_btn.clicked.connect(
            partial(self.reset_fb_filters, Ftype.BAND)
        )

#       Manage category filters

        # Order matters!
        self.cat_filter_btns = [
            self.military_btn,
            self.radar_btn,
            self.active_btn,
            self.inactive_btn,
            self.ham_btn,
            self.commercial_btn,
            self.aviation_btn,
            self.marine_btn,
            self.analogue_btn,
            self.digital_btn,
            self.trunked_btn,
            self.utility_btn,
            self.sat_btn,
            self.navigation_btn,
            self.interfering_btn,
            self.number_stations_btn,
            self.time_signal_btn
        ]

        self.apply_remove_cat_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_cat_filter_btn.set_slave_filters(
            simple_ones=[
                *self.cat_filter_btns,
                self.cat_at_least_one,
                self.cat_all
            ]
        )
        self.apply_remove_cat_filter_btn.clicked.connect(self.display_signals)
        self.reset_cat_filters_btn.clicked.connect(self.reset_cat_filters)

# #######################################################################################

        self.reset_filters_btn.clicked.connect(self.reset_all_filters)

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

        # Set mode TreeView

        self.set_mode_tree_widget()
        self.mode_tree_widget.itemSelectionChanged.connect(self.manage_mode_selections)
        self.reset_mode_filters_btn.clicked.connect(self.reset_mode_filters)
        self.apply_remove_mode_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_mode_filter_btn.set_slave_filters(
            simple_ones=[
                self.mode_tree_widget,
                self.include_unknown_modes_btn
            ]
        )
        self.apply_remove_mode_filter_btn.clicked.connect(self.display_signals)

        # Set modulation filter screen.

        self.search_bar_modulation.textEdited.connect(self.show_matching_modulations)
        self.apply_remove_modulation_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_modulation_filter_btn.set_slave_filters(
            simple_ones=[
                self.search_bar_modulation,
                self.modulation_list
            ]
        )
        self.apply_remove_modulation_filter_btn.clicked.connect(self.display_signals)
        self.reset_modulation_filters_btn.clicked.connect(self.reset_modulation_filters)
        self.modulation_list.itemClicked.connect(self.remove_if_unselected_modulation)

        # Set location filter screen.

        self.search_bar_location.textEdited.connect(self.show_matching_locations)
        self.apply_remove_location_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_location_filter_btn.set_slave_filters(
            simple_ones=[
                self.search_bar_location,
                self.locations_list
            ]
        )
        self.apply_remove_location_filter_btn.clicked.connect(self.display_signals)
        self.reset_location_filters_btn.clicked.connect(self.reset_location_filters)
        self.locations_list.itemClicked.connect(self.remove_if_unselected_location)

        # Set ACF filter screen.
        self.apply_remove_acf_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_acf_filter_btn.set_slave_filters(
            simple_ones=[
                self.include_undef_acf,
                self.acf_spinbox,
                self.acf_confidence
            ]
        )
        self.apply_remove_acf_filter_btn.clicked.connect(self.display_signals)
        self.reset_acf_filters_btn.clicked.connect(self.reset_acf_filters)
        self.acf_info_btn.clicked.connect(lambda: webbrowser.open(Constants.ACF_DOCS))

        connect_events_to_func(
            events_to_connect=[self.acf_spinbox.valueChanged,
                               self.acf_confidence.valueChanged],
            fun_to_connect=self.set_acf_interval_label,
            fun_args=None
        )

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

        # Space weather
        self.info_now_btn.clicked.connect(
            lambda: webbrowser.open(Constants.SPACE_WEATHER_INFO)
        )
        self.update_now_bar.clicked.connect(self.start_update_space_weather)
        self.update_now_bar.set_idle()
        self.space_weather_data = SpaceWeatherData()
        self.space_weather_data.update_complete.connect(self.update_space_weather)

        # Forecast
        self.forecast_info_btn.clicked.connect(
            lambda: webbrowser.open(Constants.SPACE_WEATHER_INFO)
        )
        self.forecast_data = ForecastData(self)
        self.update_forecast_bar.clicked.connect(self.start_update_forecast)
        self.update_forecast_bar.set_idle()
        self.forecast_data.update_complete.connect(self.update_forecast)


# Final operations.
        self.theme_manager.start()
        self.load_db()
        self.display_signals()

    @pyqtSlot()
    def set_visible_tab(self):
        if self.main_tab.currentWidget() != self.signal_properties_tab:
            self.main_tab.setCurrentWidget(self.signal_properties_tab)
        else:
            self.main_tab.setCurrentWidget(self.filter_tab)

    @pyqtSlot()
    def start_update_forecast(self):
        """Start the update of the 3-day forecast screen.

        Start the corresponding thread.
        """
        if not self.forecast_data.is_updating:
            self.update_forecast_bar.set_updating()
            self.forecast_data.update()

    @pyqtSlot()
    def start_update_space_weather(self):
        """Start the update of the space weather screen.

        Start the corresponding thread.
        """
        if not self.space_weather_data.is_updating:
            self.update_now_bar.set_updating()
            self.space_weather_data.update()

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

    @pyqtSlot(bool)
    def update_space_weather(self, status_ok):
        """Update the space weather screen after a successful download.

        If the download was not successful throw a warning. In any case remove
        the downloaded data.
        """
        self.update_now_bar.set_idle()
        if status_ok:
            xray_long = safe_cast(self.space_weather_data.xray[-1][7], float)

            def format_text(letter, power):
                return letter + f"{xray_long * 10**power:.1f}"

            if xray_long < 1e-8 and xray_long != -1.00e+05:
                self.peak_flux_lbl.setText(format_text("<A", 8))
            elif xray_long >= 1e-8 and xray_long < 1e-7:
                self.peak_flux_lbl.setText(format_text("A", 8))
            elif xray_long >= 1e-7 and xray_long < 1e-6:
                self.peak_flux_lbl.setText(format_text("B", 7))
            elif xray_long >= 1e-6 and xray_long < 1e-5:
                self.peak_flux_lbl.setText(format_text("C", 6))
            elif xray_long >= 1e-5 and xray_long < 1e-4:
                self.peak_flux_lbl.setText(format_text("M", 5))
            elif xray_long >= 1e-4:
                self.peak_flux_lbl.setText(format_text("X", 4))
            elif xray_long == -1.00e+05:
                self.peak_flux_lbl.setText("No Data")

            if xray_long < 1e-5 and xray_long != -1.00e+05:
                self.switchable_r_labels.switch_on(self.r0_now_lbl)
            elif xray_long >= 1e-5 and xray_long < 5e-5:
                self.switchable_r_labels.switch_on(self.r1_now_lbl)
            elif xray_long >= 5e-5 and xray_long < 1e-4:
                self.switchable_r_labels.switch_on(self.r2_now_lbl)
            elif xray_long >= 1e-4 and xray_long < 1e-3:
                self.switchable_r_labels.switch_on(self.r3_now_lbl)
            elif xray_long >= 1e-3 and xray_long < 2e-3:
                self.switchable_r_labels.switch_on(self.r4_now_lbl)
            elif xray_long >= 2e-3:
                self.switchable_r_labels.switch_on(self.r5_now_lbl)
            elif xray_long == -1.00e+05:
                self.switchable_r_labels.switch_off_all()

            pro10 = safe_cast(self.space_weather_data.prot_el[-1][8], float)
            if pro10 < 10 and pro10 != -1.00e+05:
                self.switchable_s_labels.switch_on(self.s0_now_lbl)
            elif pro10 >= 10 and pro10 < 100:
                self.switchable_s_labels.switch_on(self.s1_now_lbl)
            elif pro10 >= 100 and pro10 < 1000:
                self.switchable_s_labels.switch_on(self.s2_now_lbl)
            elif pro10 >= 1000 and pro10 < 10000:
                self.switchable_s_labels.switch_on(self.s3_now_lbl)
            elif pro10 >= 10000 and pro10 < 100000:
                self.switchable_s_labels.switch_on(self.s4_now_lbl)
            elif pro10 >= 100000:
                self.switchable_s_labels.switch_on(self.s5_now_lbl)
            elif pro10 == -1.00e+05:
                self.switchable_s_labels.switch_off_all()

            k_index = safe_cast(
                self.space_weather_data.ak_index[8][11].replace('.', ''), int
            )
            self.k_index_lbl.setText(str(k_index))
            a_index = safe_cast(
                self.space_weather_data.ak_index[7][7].replace('.', ''), int
            )
            self.a_index_lbl.setText(str(a_index))

            if k_index == 0:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_inactive_lbl)
                self.expected_noise_lbl.setText("  S0 - S1 (<-120 dBm)  ")
            elif k_index == 1:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_very_quiet_lbl)
                self.expected_noise_lbl.setText("  S0 - S1 (<-120 dBm)  ")
            elif k_index == 2:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_quiet_lbl)
                self.expected_noise_lbl.setText("  S1 - S2 (-115 dBm)  ")
            elif k_index == 3:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_unsettled_lbl)
                self.expected_noise_lbl.setText("  S2 - S3 (-110 dBm)  ")
            elif k_index == 4:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_active_lbl)
                self.expected_noise_lbl.setText("  S3 - S4 (-100 dBm)  ")
            elif k_index == 5:
                self.switchable_g_now_labels.switch_on(self.g1_now_lbl)
                self.k_storm_labels.switch_on(self.k_min_storm_lbl)
                self.expected_noise_lbl.setText("  S4 - S6 (-90 dBm)  ")
            elif k_index == 6:
                self.switchable_g_now_labels.switch_on(self.g2_now_lbl)
                self.k_storm_labels.switch_on(self.k_maj_storm_lbl)
                self.expected_noise_lbl.setText("  S6 - S9 (-80 dBm)  ")
            elif k_index == 7:
                self.switchable_g_now_labels.switch_on(self.g3_now_lbl)
                self.k_storm_labels.switch_on(self.k_sev_storm_lbl)
                self.expected_noise_lbl.setText("  S9 - S20 (>-60 dBm)  ")
            elif k_index == 8:
                self.switchable_g_now_labels.switch_on(self.g4_now_lbl)
                self.k_storm_labels.switch_on(self.k_very_sev_storm_lbl)
                self.expected_noise_lbl.setText("  S20 - S30 (>-60 dBm)  ")
            elif k_index == 9:
                self.switchable_g_now_labels.switch_on(self.g5_now_lbl)
                self.k_storm_labels.switch_on(self.k_ex_sev_storm_lbl)
                self.expected_noise_lbl.setText("  S30+ (>>-60 dBm)  ")
            self.expected_noise_lbl.switch_on()

            if a_index >= 0 and a_index < 8:
                self.a_storm_labels.switch_on(self.a_quiet_lbl)
            elif a_index >= 8 and a_index < 16:
                self.a_storm_labels.switch_on(self.a_unsettled_lbl)
            elif a_index >= 16 and a_index < 30:
                self.a_storm_labels.switch_on(self.a_active_lbl)
            elif a_index >= 30 and a_index < 50:
                self.a_storm_labels.switch_on(self.a_min_storm_lbl)
            elif a_index >= 50 and a_index < 100:
                self.a_storm_labels.switch_on(self.a_maj_storm_lbl)
            elif a_index >= 100 and a_index < 400:
                self.a_storm_labels.switch_on(self.a_sev_storm_lbl)

            index = self.space_weather_data.geo_storm[6].index("was") + 1
            k_index_24_hmax = safe_cast(
                self.space_weather_data.geo_storm[6][index], int
            )
            if k_index_24_hmax == 0:
                self.switchable_g_today_labels.switch_on(self.g0_today_lbl)
            elif k_index_24_hmax == 1:
                self.switchable_g_today_labels.switch_on(self.g0_today_lbl)
            elif k_index_24_hmax == 2:
                self.switchable_g_today_labels.switch_on(self.g0_today_lbl)
            elif k_index_24_hmax == 3:
                self.switchable_g_today_labels.switch_on(self.g0_today_lbl)
            elif k_index_24_hmax == 4:
                self.switchable_g_today_labels.switch_on(self.g0_today_lbl)
            elif k_index_24_hmax == 5:
                self.switchable_g_today_labels.switch_on(self.g1_today_lbl)
            elif k_index_24_hmax == 6:
                self.switchable_g_today_labels.switch_on(self.g2_today_lbl)
            elif k_index_24_hmax == 7:
                self.switchable_g_today_labels.switch_on(self.g3_today_lbl)
            elif k_index_24_hmax == 8:
                self.switchable_g_today_labels.switch_on(self.g4_today_lbl)
            elif k_index_24_hmax == 9:
                self.switchable_g_today_labels.switch_on(self.g5_today_lbl)

            val = safe_cast(
                self.space_weather_data.ak_index[7][2].replace('.', ''), int
            )
            self.sfi_lbl.setText(f"{val}")
            val = safe_cast(
                [x[4] for x in self.space_weather_data.sgas
                    if "SSN" in x][0], int
            )
            self.sn_lbl.setText(f"{val:d}")

            for label, pixmap in zip(self.space_weather_labels,
                                     self.space_weather_data.images):
                label.pixmap = pixmap
                label.make_transparent()
                label.apply_pixmap()
        elif not self.closing:
            pop_up(self, title=Messages.BAD_DOWNLOAD,
                   text=Messages.BAD_DOWNLOAD_MSG).show()
        self.space_weather_data.remove_data()

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

    @pyqtSlot(QListWidgetItem)
    def remove_if_unselected_modulation(self, item):
        """If an item is unselected from the modulations list, hide the item."""
        if not item.isSelected():
            self.show_matching_modulations(self.search_bar_modulation.text())

    @pyqtSlot(QListWidgetItem)
    def remove_if_unselected_location(self, item):
        """If an item is unselected from the locations list, hide the item."""
        if not item.isSelected():
            self.show_matching_locations(self.search_bar_location.text())

    @pyqtSlot(str)
    def show_matching_modulations(self, text):
        """Show the modulations which matches 'text'.

        The match criterion is defined in 'show_matching_strings'."""
        self.show_matching_strings(self.modulation_list, text)

    @pyqtSlot(str)
    def show_matching_locations(self, text):
        """Show the locations which matches 'text'.

        The match criterion is defined in 'show_matching_strings'."""
        self.show_matching_strings(self.locations_list, text)

    def show_matching_strings(self, list_elements, text):
        """Show all elements of QListWidget that matches (even partially) a target text.

        Arguments:
        list_elements -- the QListWidget
        text -- the target text.
        """
        for index in range(list_elements.count()):
            item = list_elements.item(index)
            if text.lower() in item.text().lower() or item.isSelected():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def set_mode_tree_widget(self):
        """Construct the QTreeWidget for the 'Mode' screen."""
        for parent, children in Constants.MODES.items():
            iparent = QTreeWidgetItem([parent])
            self.mode_tree_widget.addTopLevelItem(iparent)
            for child in children:
                ichild = QTreeWidgetItem([child])
                iparent.addChild(ichild)
        self.mode_tree_widget.expandAll()

    def manage_mode_selections(self):
        """Rules the selection of childs items of the 'Mode' QTreeWidget.

        If a parent is selected all its children will be selected as well.
        """
        selected_items = self.mode_tree_widget.selectedItems()
        parents = Constants.MODES.keys()
        for parent in parents:
            for item in selected_items:
                if parent == item.text(0):
                    for i in range(len(Constants.MODES[parent])):
                        item.child(i).setSelected(True)

    def set_initial_size(self):
        """Handle high resolution screens.

        Set bigger sizes for all the relevant fixed-size widgets.
        Also by default set the size to 3/4 of the available space both
        vertically and horizontally.
        """
        d = QDesktopWidget().availableGeometry()
        center = d.center()
        w = d.width()
        h = d.height()
        rect = QRect()
        rect.setHeight((3 * h) // 4)
        rect.setWidth((3 * w) // 4)
        rect.moveCenter(center)
        self.setGeometry(rect)
        if w > 3000 or h > 2000:
            self.fixed_audio_and_image.setFixedSize(540, 1150)
            self.fixed_audio_and_image.setMaximumSize(540, 1150)
            self.play.setFixedSize(140, 140)
            self.pause.setFixedSize(140, 140)
            self.stop.setFixedSize(140, 140)
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
            self.db = self.db.groupby(level=0).first()
            self.signal_names = self.db.index
            self.total_signals = len(self.signal_names)
            self.db.fillna(Constants.UNKNOWN, inplace=True)
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
    def set_min_value_upper_limit(self, lower_combo_box,
                                  lower_spin_box,
                                  upper_combo_box,
                                  upper_spin_box):
        """Forbid to a lower limit to be greater than the corresponding upper one.

        Used for frequency and bandwidth screens."""
        if lower_spin_box.isEnabled():
            unit_conversion = {'Hz': ['kHz', 'MHz', 'GHz'],
                               'kHz': ['MHz', 'GHz'],
                               'MHz': ['GHz']}
            lower_units = lower_combo_box.currentText()
            upper_units = upper_combo_box.currentText()
            lower_value = lower_spin_box.value()
            inf_limit = (lower_value * Constants.CONVERSION_FACTORS[lower_units]) \
                // Constants.CONVERSION_FACTORS[upper_units]
            counter = 0
            while inf_limit > upper_spin_box.maximum():
                counter += 1
                inf_limit //= 1000
            if upper_spin_box.minimum() != inf_limit:
                upper_spin_box.setMinimum(inf_limit)
            if counter > 0:
                new_unit = unit_conversion[upper_units][counter - 1]
                upper_combo_box.disconnect()
                upper_combo_box.setCurrentText(new_unit)
                upper_combo_box.currentTextChanged.connect(
                    partial(
                        self.set_min_value_upper_limit,
                        lower_combo_box,
                        lower_spin_box,
                        upper_combo_box,
                        upper_spin_box
                    )
                )

    @pyqtSlot()
    def set_band_filter_label(self,
                              activate_low_btn,
                              lower_spinbox,
                              lower_unit,
                              lower_confidence,
                              activate_up_btn,
                              upper_spinbox,
                              upper_unit,
                              upper_confidence,
                              range_lbl):
        """Display the actual range applied for the signal's property search.

        Used for frequency and bandwidth screens."""
        activate_low = False
        activate_high = False
        color = self.inactive_color
        title = ''
        to_display = ''
        if activate_low_btn.isChecked():
            activate_low = True
            color = self.active_color
            min_value = lower_spinbox.value()
            if lower_confidence.value() != 0:
                min_value -= lower_spinbox.value() * lower_confidence.value() / 100
            to_display += str(round(min_value, Constants.MAX_DIGITS)) \
                + ' ' + lower_unit.currentText()
        else:
            to_display += 'DC'
        to_display += Constants.RANGE_SEPARATOR
        if activate_up_btn.isChecked():
            max_value = upper_spinbox.value()
            activate_high = True
            color = self.active_color
            if upper_confidence.value() != 0:
                max_value += upper_spinbox.value() * upper_confidence.value() / 100
            to_display += str(round(max_value, Constants.MAX_DIGITS)) + ' ' \
                + upper_unit.currentText()
        else:
            to_display += 'INF'
        if activate_low and activate_high:
            title = 'Band-pass\n\n'
        elif activate_low and not activate_high:
            title = 'Low-pass\n\n'
        elif not activate_low and activate_high:
            title = 'High-pass\n\n'
        else:
            title = "Selected range:\n\n"
            to_display = "Inactive"
        to_display = title + to_display
        range_lbl.setText(to_display)
        range_lbl.setStyleSheet(f'color: {color};')

    @pyqtSlot()
    def set_acf_interval_label(self):
        """Display the actual acf interval for the search."""
        tolerance = self.acf_spinbox.value() * self.acf_confidence.value() / 100
        if tolerance > 0:
            val = round(self.acf_spinbox.value() - tolerance, Constants.MAX_DIGITS)
            to_display = f"Selected range:\n\n{val}" + Constants.RANGE_SEPARATOR \
                + f"{round(self.acf_spinbox.value() + tolerance, Constants.MAX_DIGITS)} ms"
        else:
            to_display = f"Selected value:\n\n{self.acf_spinbox.value()} ms"
        self.acf_range_lbl.setText(to_display)
        self.acf_range_lbl.setStyleSheet(f"color: {self.active_color}")

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
            if all([text.lower() in signal_name.lower(),
                    self.frequency_filters_ok(signal_name),
                    self.band_filters_ok(signal_name),
                    self.category_filters_ok(signal_name),
                    self.mode_filters_ok(signal_name),
                    self.modulation_filters_ok(signal_name),
                    self.location_filters_ok(signal_name),
                    self.acf_filters_ok(signal_name)]):
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

    @pyqtSlot()
    def reset_fb_filters(self, ftype):
        """Reset the Frequency or Bandwidth depending on 'ftype'.

        ftype can be either Ftype.FREQ or Ftype.BAND.
        """
        if ftype != Ftype.FREQ and ftype != Ftype.BAND:
            raise ValueError("Wrong ftype in function 'reset_fb_filters'")

        apply_remove_btn  = getattr(self, 'apply_remove_'  + ftype + '_filter_btn')
        include_undef_btn = getattr(self, 'include_undef_' + ftype + 's')
        activate_low      = getattr(self, 'activate_low_'  + ftype + '_filter_btn')
        activate_up       = getattr(self, 'activate_up_'   + ftype + '_filter_btn')
        lower_unit        = getattr(self, 'lower_'         + ftype + '_filter_unit')
        upper_unit        = getattr(self, 'upper_'         + ftype + '_filter_unit')
        lower_spinbox     = getattr(self, 'lower_'         + ftype + '_spinbox')
        upper_spinbox     = getattr(self, 'upper_'         + ftype + '_spinbox')
        lower_confidence  = getattr(self, 'lower_'         + ftype + '_confidence')
        upper_confidence  = getattr(self, 'lower_'         + ftype + '_confidence')

        default_val = 1 if ftype == Ftype.FREQ else 5000
        if ftype == Ftype.FREQ:
            for f in self.frequency_filters_btns:
                if f.isChecked():
                    f.setChecked(False)
        uncheck_and_emit(apply_remove_btn)
        if include_undef_btn.isChecked():
            include_undef_btn.setChecked(False)
        uncheck_and_emit(activate_low)
        uncheck_and_emit(activate_up)
        lower_unit.setCurrentText("MHz")
        upper_unit.setCurrentText("MHz")
        lower_spinbox.setValue(default_val)
        upper_spinbox.setMinimum(1)
        upper_spinbox.setValue(default_val)
        lower_confidence.setValue(0)
        upper_confidence.setValue(0)

    @pyqtSlot()
    def reset_cat_filters(self):
        """Reset the category filter screen."""
        uncheck_and_emit(self.apply_remove_cat_filter_btn)
        for f in self.cat_filter_btns:
            if f.isChecked():
                f.setChecked(False)
        self.cat_at_least_one.setChecked(True)

    @pyqtSlot()
    def reset_mode_filters(self):
        """Reset the mode filter screen."""
        uncheck_and_emit(self.apply_remove_mode_filter_btn)
        parents = Constants.MODES.keys()
        selected_children = []
        for item in self.mode_tree_widget.selectedItems():
            if item.text(0) in parents:
                item.setSelected(False)
            else:
                selected_children.append(item)
        for children in selected_children:
            children.setSelected(False)
        if self.include_unknown_modes_btn.isChecked():
            self.include_unknown_modes_btn.setChecked(False)

    @pyqtSlot()
    def reset_modulation_filters(self):
        """Reset the modulation filter screen."""
        uncheck_and_emit(self.apply_remove_modulation_filter_btn)
        self.search_bar_modulation.setText('')
        self.show_matching_strings(
            self.modulation_list,
            self.search_bar_modulation.text()
        )
        for i in range(self.modulation_list.count()):
            if self.modulation_list.item(i).isSelected():
                self.modulation_list.item(i).setSelected(False)

    @pyqtSlot()
    def reset_location_filters(self):
        """Reset the location filter screen."""
        uncheck_and_emit(self.apply_remove_location_filter_btn)
        self.search_bar_location.setText('')
        self.show_matching_strings(
            self.locations_list,
            self.search_bar_location.text()
        )
        for i in range(self.locations_list.count()):
            if self.locations_list.item(i).isSelected():
                self.locations_list.item(i).setSelected(False)

    @pyqtSlot()
    def reset_acf_filters(self):
        """Reset the acf filter screen."""
        uncheck_and_emit(self.apply_remove_acf_filter_btn)
        if self.include_undef_acf.isChecked():
            self.include_undef_acf.setChecked(False)
        self.acf_spinbox.setValue(50)
        self.acf_confidence.setValue(0)

    def frequency_filters_ok(self, signal_name):
        """Evalaute if the signal matches the frequency filters."""
        if not self.apply_remove_freq_filter_btn.isChecked():
            return True
        undef_freq = is_undef_freq(self.db.loc[signal_name])
        if undef_freq:
            if self.include_undef_freqs.isChecked():
                return True
            else:
                return False

        signal_freqs = (
            safe_cast(self.db.at[signal_name, Signal.INF_FREQ], int),
            safe_cast(self.db.at[signal_name, Signal.SUP_FREQ], int)
        )

        band_filter_ok = False
        any_checked = False
        for btn, band_limits in zip(self.frequency_filters_btns, Constants.BANDS):
            if btn.isChecked():
                any_checked = True
                if signal_freqs[0] < band_limits.upper and signal_freqs[1] >= band_limits.lower:
                    band_filter_ok = True
        lower_limit_ok = True
        upper_limit_ok = True
        if self.activate_low_freq_filter_btn.isChecked():
            if not signal_freqs[1] >= filters_limit(self.lower_freq_spinbox,
                                                    self.lower_freq_filter_unit,
                                                    self.lower_freq_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_freq_filter_btn.isChecked():
            if not signal_freqs[0] < filters_limit(self.upper_freq_spinbox,
                                                   self.upper_freq_filter_unit,
                                                   self.upper_freq_confidence):
                upper_limit_ok = False
        if any_checked:
            return band_filter_ok and lower_limit_ok and upper_limit_ok
        else:
            return lower_limit_ok and upper_limit_ok

    def band_filters_ok(self, signal_name):
        """Evalaute if the signal matches the band filters."""
        if not self.apply_remove_band_filter_btn.isChecked():
            return True
        undef_band = is_undef_band(self.db.loc[signal_name])
        if undef_band:
            if self.include_undef_bands.isChecked():
                return True
            else:
                return False

        signal_bands = (
            safe_cast(self.db.at[signal_name, Signal.INF_BAND], int),
            safe_cast(self.db.at[signal_name, Signal.SUP_BAND], int)
        )

        lower_limit_ok = True
        upper_limit_ok = True
        if self.activate_low_band_filter_btn.isChecked():
            if not signal_bands[1] >= filters_limit(self.lower_band_spinbox,
                                                    self.lower_band_filter_unit,
                                                    self.lower_band_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_band_filter_btn.isChecked():
            if not signal_bands[0] < filters_limit(self.upper_band_spinbox,
                                                   self.upper_band_filter_unit,
                                                   self.upper_band_confidence):
                upper_limit_ok = False
        return lower_limit_ok and upper_limit_ok

    def category_filters_ok(self, signal_name):
        """Evalaute if the signal matches the category filters."""
        if not self.apply_remove_cat_filter_btn.isChecked():
            return True
        cat_code = self.db.at[signal_name, Signal.CATEGORY_CODE]
        cat_checked = 0
        positive_cases = 0
        for index, cat in enumerate(self.cat_filter_btns):
            if cat.isChecked():
                cat_checked += 1
                if cat_code[index] == '1':
                    positive_cases += 1
        if self.cat_at_least_one.isChecked():
            return positive_cases > 0
        else:
            return cat_checked == positive_cases and cat_checked > 0

    def mode_filters_ok(self, signal_name):
        """Evalaute if the signal matches the mode filters."""
        if not self.apply_remove_mode_filter_btn.isChecked():
            return True
        signal_mode = self.db.at[signal_name, Signal.MODE]
        if signal_mode == Constants.UNKNOWN:
            if self.include_unknown_modes_btn.isChecked():
                return True
            else:
                return False
        selected_items = [item for item in self.mode_tree_widget.selectedItems()]
        selected_items_text = [i.text(0) for i in selected_items]
        parents = [
            item for item in selected_items_text
            if item in Constants.MODES.keys()
        ]
        ok = []
        for item in selected_items:
            if item.text(0) in parents:
                ok.append(item.text(0) in signal_mode)
            elif not item.parent().isSelected():
                ok.append(item.text(0) == signal_mode)
        return any(ok)

    def get_field_entries(self, signal_name, field, separator=Constants.FIELD_SEPARATOR):
        """Take a signal name, a column label and optionally a separator string.

        Return a list obtained by splitting the signal field with separator."""
        return [
            x.strip() for x in self.db.at[signal_name, field].split(separator)
        ]

    def modulation_filters_ok(self, signal_name):
        """Evalaute if the signal matches the modulation filters."""
        if not self.apply_remove_modulation_filter_btn.isChecked():
            return True
        signal_modulation = self.get_field_entries(
            signal_name, Signal.MODULATION
        )
        for item in self.modulation_list.selectedItems():
            if item.text() in signal_modulation:
                return True
        return False

    def location_filters_ok(self, signal_name):
        """Evalaute if the signal matches the location filters."""
        if not self.apply_remove_location_filter_btn.isChecked():
            return True
        signal_locations = self.get_field_entries(
            signal_name, Signal.LOCATION
        )
        for item in self.locations_list.selectedItems():
            if item.text() in signal_locations:
                return True
        return False

    def acf_filters_ok(self, signal_name):
        """Evalaute if the signal matches the acf filters."""
        if not self.apply_remove_acf_filter_btn.isChecked():
            return True
        signal_acf = self.db.at[signal_name, Signal.ACF]
        if signal_acf == Constants.UNKNOWN:
            if self.include_undef_acf.isChecked():
                return True
            else:
                return False
        else:
            signal_acf = safe_cast(signal_acf.rstrip("ms"), float)
            tolerance = self.acf_spinbox.value() * self.acf_confidence.value() / 100
            upper_limit = self.acf_spinbox.value() + tolerance
            lower_limit = self.acf_spinbox.value() - tolerance
            if signal_acf <= upper_limit and signal_acf >= lower_limit:
                return True
            else:
                return False

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
            self.acf_lab.setText(current_signal.at[Signal.ACF])
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
    def reset_all_filters(self):
        """Reset all filter screens.

        Show all available signals.
        """
        self.reset_frequency_filters_btn.clicked.emit()
        self.reset_band_filters_btn.clicked.emit()
        self.reset_cat_filters_btn.clicked.emit()
        self.reset_mode_filters_btn.clicked.emit()
        self.reset_modulation_filters_btn.clicked.emit()
        self.reset_location_filters_btn.clicked.emit()
        self.reset_acf_filters_btn.clicked.emit()

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
