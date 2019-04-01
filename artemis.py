from collections import namedtuple
from itertools import chain
from functools import partial
from glob import glob
import webbrowser
import os
import sys
from time import sleep

from pandas import read_csv
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             qApp,
                             QDesktopWidget,
                             QListWidgetItem,
                             QMessageBox,
                             QSplashScreen,
                             QTreeView,
                             QTreeWidgetItem,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import (QFileInfo,
                          Qt,
                          pyqtSlot,)

from audio_player import AudioPlayer
from space_weather_data import SpaceWeatherData
from double_text_button import DoubleTextButton
from download_window import DownloadWindow
from switchable_label import SwitchableLabel, SwitchableLabelsIterable
from constants import (Constants,
                       Ftype,
                       GfdType,
                       Database,
                       ChecksumWhat,
                       Messages,
                       Signal,
                       Colors,)
from themes import Theme
from utilities import (checksum_ok,
                       uncheck_and_emit,
                       pop_up,
                       connect_to,
                       filters_ok,
                       is_undef_freq,
                       is_undef_band,
                       change_unit,
                       format_numbers,
                       resource_path,)

import icon_rc

qt_creator_file = resource_path("artemis.ui")
Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)


class Artemis(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_initial_size()
        self.download_window = DownloadWindow()
        self.actionExit.triggered.connect(qApp.quit)
        self.action_update_database.triggered.connect(self.ask_if_download)
        self.action_check_db_ver.triggered.connect(self.check_db_ver)
        self.db = None
        self.current_signal_name = ''
        self.signal_names = []
        self.total_signals = 0
        self.theme = Theme(self)

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

        connect_to(
            events_to_connect = [self.lower_freq_spinbox.valueChanged,
                                 self.upper_freq_spinbox.valueChanged,
                                 self.lower_freq_filter_unit.currentTextChanged,
                                 self.upper_freq_filter_unit.currentTextChanged,
                                 self.activate_low_freq_filter_btn.toggled],
            fun_to_connect = self.set_min_value_upper_limit,
            fun_args = [self.lower_freq_filter_unit,
                        self.lower_freq_spinbox,
                        self.upper_freq_filter_unit,
                        self.upper_freq_spinbox]
        )

        connect_to(
            events_to_connect = [self.lower_freq_spinbox.valueChanged,
                                 self.upper_freq_spinbox.valueChanged,
                                 self.lower_freq_filter_unit.currentTextChanged,
                                 self.upper_freq_filter_unit.currentTextChanged,
                                 self.activate_low_freq_filter_btn.clicked,
                                 self.activate_up_freq_filter_btn.clicked,
                                 self.lower_freq_confidence.valueChanged,
                                 self.upper_freq_confidence.valueChanged],
            fun_to_connect = self.set_band_filter_label,
            fun_args = [self.activate_low_freq_filter_btn,
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
            [
                *self.frequency_filters_btns,
                self.include_undef_freqs,
                self.activate_low_freq_filter_btn,
                self.activate_up_freq_filter_btn,
            ],
            self.activate_low_freq_filter_btn,
            [
                self.lower_freq_spinbox,
                self.lower_freq_filter_unit,
                self.lower_freq_confidence,
            ],
            self.activate_up_freq_filter_btn,
            [
                self.upper_freq_spinbox,
                self.upper_freq_filter_unit,
                self.upper_freq_confidence,
            ],
        )
        self.apply_remove_freq_filter_btn.clicked.connect(self.display_signals)
        self.reset_frequency_filters_btn.clicked.connect(partial(self.reset_fb_filters, Ftype.FREQ))

        # Manage bandwidth filters.

        connect_to(
            events_to_connect = [self.lower_band_spinbox.valueChanged,
                                 self.upper_band_spinbox.valueChanged,
                                 self.lower_band_filter_unit.currentTextChanged,
                                 self.upper_band_filter_unit.currentTextChanged,
                                 self.activate_low_band_filter_btn.toggled],
            fun_to_connect = self.set_min_value_upper_limit,
            fun_args = [self.lower_band_filter_unit,
                        self.lower_band_spinbox,
                        self.upper_band_filter_unit,
                        self.upper_band_spinbox]
        )

        connect_to(
            events_to_connect = [self.lower_band_spinbox.valueChanged,
                                 self.upper_band_spinbox.valueChanged,
                                 self.lower_band_filter_unit.currentTextChanged,
                                 self.upper_band_filter_unit.currentTextChanged,
                                 self.activate_low_band_filter_btn.clicked,
                                 self.activate_up_band_filter_btn.clicked,
                                 self.lower_band_confidence.valueChanged,
                                 self.upper_band_confidence.valueChanged],
            fun_to_connect = self.set_band_filter_label,
            fun_args = [self.activate_low_band_filter_btn,
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

        self.apply_remove_band_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_band_filter_btn.set_slave_filters(
            [
                self.include_undef_bands,
                self.activate_low_band_filter_btn,
                self.activate_up_band_filter_btn,
            ],
            self.activate_low_band_filter_btn,
            [
                self.lower_band_spinbox,
                self.lower_band_filter_unit,
                self.lower_band_confidence,
            ],
            self.activate_up_band_filter_btn,
            [
                self.upper_band_spinbox,
                self.upper_band_filter_unit,
                self.upper_band_confidence,
            ],
        )
        self.apply_remove_band_filter_btn.clicked.connect(self.display_signals)
        self.reset_band_filters_btn.clicked.connect(partial(self.reset_fb_filters, Ftype.BAND))

#       Manage category filters

        # Order matters!
        self.cat_filter_btns = [self.military_btn,
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
                                self.time_signal_btn,]

        self.apply_remove_cat_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_cat_filter_btn.set_slave_filters([*self.cat_filter_btns,
                                                             self.cat_at_least_one,
                                                             self.cat_all])
        self.apply_remove_cat_filter_btn.clicked.connect(self.display_signals)
        self.reset_cat_filters_btn.clicked.connect(self.reset_cat_filters)

# #######################################################################################

        self.reset_filters_btn.clicked.connect(self.reset_all_filters)

        UrlColors = namedtuple("UrlColors", ["inactive", "active", "clicked"])
        self.url_button.colors = UrlColors("#9f9f9f", "#4c75ff", "#942ccc")
        self.category_labels = [self.cat_mil,
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
                                self.cat_time_sig,]

        self.property_labels = [self.freq_lab,
                                self.band_lab,
                                self.mode_lab,
                                self.modul_lab,
                                self.loc_lab,
                                self.acf_lab,
                                self.description_text,]

        self.url_button.clicked.connect(self.go_to_web_page_signal)

        # Set mode TreeView

        self.set_mode_tree_widget()
        self.mode_tree_widget.itemSelectionChanged.connect(self.manage_mode_selections)
        self.reset_mode_filters_btn.clicked.connect(self.reset_mode_filters)
        self.apply_remove_mode_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_mode_filter_btn.set_slave_filters([self.mode_tree_widget,
                                                             self.include_unknown_modes_btn])
        self.apply_remove_mode_filter_btn.clicked.connect(self.display_signals)

        # Set modulation filter screen.

        self.modulation_list.addItems(Constants.MODULATIONS)
        self.search_bar_modulation.textEdited.connect(self.show_matching_modulations)
        self.apply_remove_modulation_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_modulation_filter_btn.set_slave_filters([self.search_bar_modulation,
                                                                   self.modulation_list])
        self.apply_remove_modulation_filter_btn.clicked.connect(self.display_signals)
        self.reset_modulation_filters_btn.clicked.connect(self.reset_modulation_filters)
        self.modulation_list.itemClicked.connect(self.remove_if_unselected_modulation)

        # Set location filter screen.

        self.locations_list.addItems(Constants.LOCATIONS)
        self.search_bar_location.textEdited.connect(self.show_matching_locations)
        self.apply_remove_location_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_location_filter_btn.set_slave_filters([self.search_bar_location,
                                                                 self.locations_list])
        self.apply_remove_location_filter_btn.clicked.connect(self.display_signals)
        self.reset_location_filters_btn.clicked.connect(self.reset_location_filters)
        self.locations_list.itemClicked.connect(self.remove_if_unselected_location)

        # Set ACF filter screen.
        self.apply_remove_acf_filter_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_acf_filter_btn.set_slave_filters([self.include_undef_acf, self.acf_spinbox, self.acf_confidence])
        self.apply_remove_acf_filter_btn.clicked.connect(self.display_signals)
        self.reset_acf_filters_btn.clicked.connect(self.reset_acf_filters)
        self.acf_info_btn.clicked.connect(lambda : webbrowser.open(Constants.ACF_DOCS))

        connect_to(
            events_to_connect = [self.acf_spinbox.valueChanged, self.acf_confidence.valueChanged],
            fun_to_connect = self.set_acf_interval_label,
            fun_args = None
        )

        # GFD
        self.freq_search_gfd_btn.clicked.connect(partial(self.go_to_gfd, GfdType.FREQ))
        self.location_search_gfd_btn.clicked.connect(partial(self.go_to_gfd, GfdType.LOC))
        self.gfd_line_edit.returnPressed.connect(partial(self.go_to_gfd, GfdType.LOC))

# ##########################################################################################

        # Left list widget and search bar.
        self.search_bar.textChanged.connect(self.display_signals)
        self.result_list.currentItemChanged.connect(self.display_specs)
        self.result_list.itemDoubleClicked.connect(lambda: self.main_tab.setCurrentWidget(self.signal_properties_tab))
        self.audio_widget = AudioPlayer(self.play,
                                        self.pause,
                                        self.stop,
                                        self.volume,
                                        self.audio_progress,
                                        self.active_color,
                                        self.inactive_color)

        BandLabel = namedtuple("BandLabel", ["left", "center", "right"])
        self.band_labels = [
            BandLabel(self.elf_left, self.elf, self.elf_right),
            BandLabel(self.slf_left, self.slf, self.slf_right),
            BandLabel(self.ulf_left, self.ulf, self.ulf_right),
            BandLabel(self.vlf_left, self.vlf, self.vlf_right),
            BandLabel(self.lf_left,  self.lf,  self.lf_right),
            BandLabel(self.mf_left,  self.mf,  self.mf_right),
            BandLabel(self.hf_left,  self.hf,  self.hf_right),
            BandLabel(self.vhf_left, self.vhf, self.vhf_right),
            BandLabel(self.uhf_left, self.uhf, self.uhf_right),
            BandLabel(self.shf_left, self.shf, self.shf_right),
            BandLabel(self.ehf_left, self.ehf, self.ehf_right),
        ]

        # Space weather
        self.info_now_btn.clicked.connect(lambda : webbrowser.open(Constants.FORECAST_INFO))
        self.update_now_btn.clicked.connect(self.start_update_space_weather)
        self.space_weather_data = SpaceWeatherData()
        self.space_weather_data.update_complete.connect(self.update_space_weather)
        self.switchable_r_labels = SwitchableLabelsIterable(self.r0_now_lbl,
                                                            self.r1_now_lbl,
                                                            self.r2_now_lbl,
                                                            self.r3_now_lbl,
                                                            self.r4_now_lbl,
                                                            self.r5_now_lbl,)
        self.switchable_s_labels = SwitchableLabelsIterable(self.s0_now_lbl,
                                                            self.s1_now_lbl,
                                                            self.s2_now_lbl,
                                                            self.s3_now_lbl,
                                                            self.s4_now_lbl,
                                                            self.s5_now_lbl,)
        self.switchable_g_now_labels = SwitchableLabelsIterable(self.g0_now_lbl,
                                                                self.g1_now_lbl,
                                                                self.g2_now_lbl,
                                                                self.g3_now_lbl,
                                                                self.g4_now_lbl,
                                                                self.g5_now_lbl)
        self.switchable_g_today_labels = SwitchableLabelsIterable(self.g0_today_lbl,
                                                                  self.g1_today_lbl,
                                                                  self.g2_today_lbl,
                                                                  self.g3_today_lbl,
                                                                  self.g4_today_lbl,
                                                                  self.g5_today_lbl)
        colors_array = [[Colors.WHITE_LIGHT,  Colors.WHITE_DARK],
                        [Colors.BLUE_LIGHT,   Colors.BLUE_DARK],
                        [Colors.GREEN_LIGHT,  Colors.GREEN_DARK],
                        [Colors.YELLOW_LIGHT, Colors.YELLOW_DARK],
                        [Colors.ORANGE_LIGHT, Colors.ORANGE_DARK],
                        [Colors.RED_LIGHT, Colors.RED_DARK]]

        for lab, [light_color, dark_color] in zip(chain(self.switchable_r_labels,
                                                        self.switchable_s_labels,
                                                        self.switchable_g_now_labels,
                                                        self.switchable_g_today_labels),
                                                  colors_array * 4):
            lab.set_colors(light_color, dark_color)

        k_storms_colors = [[Colors.RED_LIGHT, Colors.RED_DARK],
                           [Colors.RED2_LIGHT, Colors.RED2_DARK],
                           [Colors.RED3_LIGHT, Colors.RED3_DARK],
                           [Colors.ORANGE_LIGHT, Colors.ORANGE_DARK],
                           [Colors.ORANGE2_LIGHT, Colors.ORANGE2_DARK],
                           [Colors.YELLOW_LIGHT, Colors.YELLOW_DARK],
                           [Colors.GREEN3_LIGHT, Colors.GREEN3_DARK],
                           [Colors.GREEN2_LIGHT, Colors.GREEN2_DARK],
                           [Colors.GREEN_LIGHT, Colors.GREEN_DARK],
                           [Colors.BLUE_LIGHT, Colors.BLUE_DARK]]
        a_storm_colors = [[Colors.RED_LIGHT, Colors.RED_DARK],
                          [Colors.ORANGE_LIGHT, Colors.ORANGE_DARK],
                          [Colors.ORANGE2_LIGHT, Colors.ORANGE2_DARK],
                          [Colors.YELLOW_LIGHT, Colors.YELLOW_DARK],
                          [Colors.GREEN_LIGHT, Colors.GREEN_DARK],
                          [Colors.BLUE_LIGHT, Colors.BLUE_DARK]]

        self.k_storm_labels = SwitchableLabelsIterable(self.k_ex_sev_storm_lbl,
                                                       self.k_very_sev_storm_lbl,
                                                       self.k_sev_storm_lbl,
                                                       self.k_maj_storm_lbl,
                                                       self.k_min_storm_lbl,
                                                       self.k_active_lbl,
                                                       self.k_unsettled_lbl,
                                                       self.k_quiet_lbl,
                                                       self.k_very_quiet_lbl,
                                                       self.k_inactive_lbl)
        self.a_storm_labels = SwitchableLabelsIterable(self.a_sev_storm_lbl,
                                                       self.a_maj_storm_lbl,
                                                       self.a_min_storm_lbl,
                                                       self.a_active_lbl,
                                                       self.a_unsettled_lbl,
                                                       self.a_quiet_lbl)

        for lab, [light_color, dark_color] in zip(chain(self.k_storm_labels, self.a_storm_labels),
                                                  chain(k_storms_colors, a_storm_colors)):
            lab.set_colors(light_color, dark_color)

# Final operations.
        self.theme.initialize()
        self.load_db()
        self.display_signals()
        self.show()

    @pyqtSlot()
    def start_update_space_weather(self):
        self.update_now_bar.setMaximum(self.update_now_bar.minimum())
        self.space_weather_data.update()

    @pyqtSlot(bool)
    def update_space_weather(self, status_ok):
        self.update_now_bar.setMaximum(self.update_now_bar.minimum() + 1)
        if status_ok:
            xray_long = float(self.space_weather_data.xray[-1][7])
            format_text = lambda letter, power : letter + f"{xray_long * 10**power:.1f}"
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

            pro10 = float(self.space_weather_data.prot_el[-1][8])
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

            k_index = int(self.space_weather_data.ak_index[8][11].replace('.', ''))
            self.k_index_lbl.setText(str(k_index))
            a_index = int(self.space_weather_data.ak_index[7][7].replace('.', ''))
            self.a_index_lbl.setText(str(a_index))

            if k_index == 0:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_inactive_lbl)
            elif k_index == 1:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_very_quiet_lbl)
            elif k_index == 2:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_quiet_lbl)
            elif k_index == 3:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_unsettled_lbl)
            elif k_index == 4:
                self.switchable_g_now_labels.switch_on(self.g0_now_lbl)
                self.k_storm_labels.switch_on(self.k_active_lbl)
            elif k_index == 5:
                self.switchable_g_now_labels.switch_on(self.g1_now_lbl)
                self.k_storm_labels.switch_on(self.k_min_storm_lbl)
            elif k_index == 6:
                self.switchable_g_now_labels.switch_on(self.g2_now_lbl)
                self.k_storm_labels.switch_on(self.k_maj_storm_lbl)
            elif k_index == 7:
                self.switchable_g_now_labels.switch_on(self.g3_now_lbl)
                self.k_storm_labels.switch_on(self.k_sev_storm_lbl)
            elif k_index == 8:
                self.switchable_g_now_labels.switch_on(self.g4_now_lbl)
                self.k_storm_labels.switch_on(self.k_very_sev_storm_lbl)
            elif k_index == 9:
                self.switchable_g_now_labels.switch_on(self.g5_now_lbl)
                self.k_storm_labels.switch_on(self.k_ex_sev_storm_lbl)

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
            k_index_24_hmax = int(self.space_weather_data.geo_storm[6][index])
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

            self.sfi_lbl.setText(self.space_weather_data.ak_index[7][2].replace('.', '').lstrip('0'))
            self.sn_lbl.setText([x[4] for i, x in enumerate(self.space_weather_data.sgas) if "SSN" in x][0].lstrip('0'))

        else:
            pop_up(self, title = Messages.BAD_DOWNLOAD,
                   text = Messages.BAD_DOWNLOAD_MSG).show()
        self.space_weather_data.remove_data()

    @pyqtSlot()
    def go_to_gfd(self, by):
        query = "/?q="
        if by is GfdType.FREQ:
            value_in_mhz = self.freq_gfd.value() * Constants.CONVERSION_FACTORS[self.unit_freq_gfd.currentText()] / Constants.CONVERSION_FACTORS["MHz"]
            query += str(value_in_mhz)
        elif by is GfdType.LOC:
            query += self.gfd_line_edit.text()
        try:
            webbrowser.open(Constants.GFD_SITE + query.lower())
        except:
            pass

    @pyqtSlot(QListWidgetItem)
    def remove_if_unselected_modulation(self, item):
        if not item.isSelected():
            self.show_matching_modulations(self.search_bar_modulation.text())

    @pyqtSlot(QListWidgetItem)
    def remove_if_unselected_location(self, item):
        if not item.isSelected():
            self.show_matching_locations(self.search_bar_location.text())

    @pyqtSlot(str)
    def show_matching_modulations(self, text):
        self.show_matching_strings(self.modulation_list, text)

    @pyqtSlot(str)
    def show_matching_locations(self, text):
        self.show_matching_strings(self.locations_list, text)

    def show_matching_strings(self, list_elements, text):
        for index in range(list_elements.count()):
            item = list_elements.item(index)
            if text.upper() in item.text() or item.isSelected():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def set_mode_tree_widget(self):
        for parent, children in Constants.MODES.items():
            iparent = QTreeWidgetItem([parent])
            self.mode_tree_widget.addTopLevelItem(iparent)
            for child in children:
                ichild = QTreeWidgetItem([child])
                iparent.addChild(ichild)
        self.mode_tree_widget.expandAll()

    def manage_mode_selections(self):
        selected_items = self.mode_tree_widget.selectedItems()
        parents = Constants.MODES.keys()
        for parent in parents:
            for item in selected_items:
                if parent == item.text(0):
                    for i in range(len(Constants.MODES[parent])):
                        item.child(i).setSelected(True)

    def set_initial_size(self):
        """
        Function to handle high resolution screens. The function sets bigger sizes
        for all the relevant fixed-size widgets.
        """
        d = QDesktopWidget().availableGeometry()
        w = d.width()
        h = d.height()
        self.setGeometry(50, 50, (3  * w) // 4, (3 * h) // 4)
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
        if not self.download_window.isVisible():
            self.download_window.download_thread.finished.connect(self.show_downloaded_signals)
            self.download_window.download_thread.start()
            self.download_window.show()

    @pyqtSlot()
    def ask_if_download(self):
        if not self.download_window.isVisible():
            db_path = os.path.join(Constants.DATA_FOLDER, Database.NAME)
            try:
                with open(db_path, "rb") as file_db:
                    db = file_db.read()
            except:
                self.download_db()
            else:
                try:
                    is_checksum_ok = checksum_ok(db, ChecksumWhat.DB)
                except:
                    pop_up(self, title = Messages.NO_CONNECTION,
                           text = Messages.NO_CONNECTION_MSG).show()
                else:
                    if not is_checksum_ok:
                        self.download_db()
                    else:
                        answer = pop_up(self, title = Messages.DB_UP_TO_DATE,
                                        text = Messages.DB_UP_TO_DATE_MSG,
                                        informative_text = Messages.DOWNLOAD_ANYWAY_QUESTION,
                                        is_question = True,
                                        default_btn = QMessageBox.No).exec()
                        if answer == QMessageBox.Yes:
                            self.download_db()

    @pyqtSlot()
    def check_db_ver(self):
        if not self.download_window.isVisible():
            db_path = os.path.join(Constants.DATA_FOLDER, Database.NAME)
            answer = None
            try:
                with open(db_path, "rb") as file_db:
                    db = file_db.read()
            except:
                answer = pop_up(self, title = Messages.NO_DB,
                                text = Messages.NO_DB_AVAIL,
                                informative_text = Messages.DOWNLOAD_NOW_QUESTION,
                                is_question = True).exec()
            else:
                try:
                    is_checksum_ok = checksum_ok(db, ChecksumWhat.DB)
                except:
                    pop_up(self, title = Messages.NO_CONNECTION,
                           text = Messages.NO_CONNECTION_MSG).show()
                else:
                    if is_checksum_ok:
                        pop_up(self, title = Messages.DB_UP_TO_DATE,
                               text = Messages.DB_UP_TO_DATE_MSG).show()

                    else:
                        answer = pop_up(self, title = Messages.DB_NEW_VER,
                                        text = Messages.DB_NEW_VER_MSG,
                                        informative_text = Messages.DOWNLOAD_NOW_QUESTION,
                                        is_question = True).exec()
                        if answer == QMessageBox.Yes:
                            self.download_db()

    @pyqtSlot()
    def show_downloaded_signals(self):
        if self.download_window.everything_ok:
            self.search_bar.setEnabled(True)
            self.load_db()
            self.display_signals()

    def load_db(self):
        names = Database.NAMES
        try:
            self.db = read_csv(os.path.join(Constants.DATA_FOLDER, Database.NAME),
                               sep = Database.DELIMITER,
                               header = None,
                               index_col = 0,
                               dtype = {name : str for name in Database.STRINGS},
                               names = names,)
        except FileNotFoundError:
            self.search_bar.setDisabled(True)
            answer = pop_up(self, title = Messages.NO_DB,
                            text = Messages.NO_DB_AVAIL,
                            informative_text = Messages.DOWNLOAD_NOW_QUESTION,
                            is_question = True).exec()
            if answer == QMessageBox.Yes:
                self.download_db()
        else:
            self.signal_names = self.db.index
            self.total_signals = len(self.signal_names)
            self.db.fillna(Constants.UNKNOWN, inplace = True)
            self.db[Signal.WIKI_CLICKED] = False
            self.update_status_tip(self.total_signals)
            self.result_list.addItems(self.signal_names)

    @pyqtSlot()
    def set_min_value_upper_limit(self, lower_combo_box,
                                  lower_spin_box,
                                  upper_combo_box,
                                  upper_spin_box):
        if lower_spin_box.isEnabled():
            unit_conversion = {'Hz' : ['kHz', 'MHz', 'GHz'],
                               'kHz': ['MHz', 'GHz'],
                               'MHz': ['GHz']}
            lower_units = lower_combo_box.currentText()
            upper_units = upper_combo_box.currentText()
            lower_value = lower_spin_box.value()
            upper_value = upper_spin_box.value()
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
                    partial(self.set_min_value_upper_limit,
                            lower_combo_box,
                            lower_spin_box,
                            upper_combo_box,
                            upper_spin_box)
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
            to_display += str(round(min_value, Constants.MAX_DIGITS)) + ' ' + lower_unit.currentText()
        else:
            to_display += 'DC'
        to_display += Constants.RANGE_SEPARATOR
        if activate_up_btn.isChecked():
            max_value = upper_spinbox.value()
            activate_high = True
            color = self.active_color
            if upper_confidence.value() != 0:
                max_value += upper_spinbox.value() * upper_confidence.value() / 100
            to_display += str(round(max_value, Constants.MAX_DIGITS)) + ' ' + upper_unit.currentText()
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
        tolerance = self.acf_spinbox.value() * self.acf_confidence.value() / 100
        if tolerance > 0:
            to_display = f"Selected range:\n\n{round(self.acf_spinbox.value() - tolerance, Constants.MAX_DIGITS)}" +\
                Constants.RANGE_SEPARATOR + f"{round(self.acf_spinbox.value() + tolerance, Constants.MAX_DIGITS)} ms"
        else:
            to_display = f"Selected value:\n\n{self.acf_spinbox.value()} ms"
        self.acf_range_lbl.setText(to_display)
        self.acf_range_lbl.setStyleSheet(f"color: {self.active_color}")

    @pyqtSlot()
    def activate_if_toggled(self, radio_btn, *widgets):
        toggled = True if radio_btn.isChecked() else False
        for w in widgets[:-1]: # Neglect the bool coming from the emitted signal.
            w.setEnabled(toggled)

    @pyqtSlot()
    def display_signals(self):
        text = self.search_bar.text()
        available_signals = 0
        for index, signal_name in enumerate(self.signal_names):
            if all([text.lower() in signal_name.lower()     ,
                    self.frequency_filters_ok(signal_name)  ,
                    self.band_filters_ok(signal_name)       ,
                    self.category_filters_ok(signal_name)   ,
                    self.mode_filters_ok(signal_name)       ,
                    self.modulation_filters_ok(signal_name) ,
                    self.location_filters_ok(signal_name)   ,
                    self.acf_filters_ok(signal_name)]):
                self.result_list.item(index).setHidden(False)
                available_signals += 1
            else:
                self.result_list.item(index).setHidden(True)
        # Remove selected item.
        self.result_list.selectionModel().clear()
        self.update_status_tip(available_signals)

    def update_status_tip(self, available_signals):
        if available_signals < self.total_signals:
            self.statusbar.setStyleSheet(f'color: {self.active_color}')
        else:
            self.statusbar.setStyleSheet(f'color: {self.inactive_color}')
        self.statusbar.showMessage(f"{available_signals} out of {self.total_signals} signals displayed.")

    @pyqtSlot()
    def reset_fb_filters(self, ftype):
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
        uncheck_and_emit(self.apply_remove_cat_filter_btn)
        for f in self.cat_filter_btns:
            if f.isChecked():
                f.setChecked(False)
        self.cat_at_least_one.setChecked(True)

    @pyqtSlot()
    def reset_mode_filters(self):
        uncheck_and_emit(self.apply_remove_mode_filter_btn)
        for item in self.mode_tree_widget.selectedItems():
            item.setSelected(False)
        if self.include_unknown_modes_btn.isChecked():
            self.include_unknown_modes_btn.setChecked(False)

    @pyqtSlot()
    def reset_modulation_filters(self):
        uncheck_and_emit(self.apply_remove_modulation_filter_btn)
        self.search_bar_modulation.setText('')
        for i in range(self.modulation_list.count()):
            if self.modulation_list.item(i).isSelected():
                self.modulation_list.item(i).setSelected(False)

    @pyqtSlot()
    def reset_location_filters(self):
        uncheck_and_emit(self.apply_remove_location_filter_btn)
        self.search_bar_location.setText('')
        for i in range(self.locations_list.count()):
            if self.locations_list.item(i).isSelected():
                self.locations_list.item(i).setSelected(False)

    @pyqtSlot()
    def reset_acf_filters(self):
        uncheck_and_emit(self.apply_remove_acf_filter_btn)
        if self.include_undef_acf.isChecked():
            self.include_undef_acf.setChecked(False)
        self.acf_spinbox.setValue(50)
        self.acf_confidence.setValue(0)

    def frequency_filters_ok(self, signal_name):
        if not self.apply_remove_freq_filter_btn.isChecked():
            return True
        undef_freq = is_undef_freq(self.db.loc[signal_name])
        if undef_freq:
            if self.include_undef_freqs.isChecked():
                return True
            else:
                return False

        signal_freqs = (int(self.db.at[signal_name, Signal.INF_FREQ]),
                        int(self.db.at[signal_name, Signal.SUP_FREQ]))

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
            if not signal_freqs[1] >= filters_ok(self.lower_freq_spinbox,
                                                 self.lower_freq_filter_unit,
                                                 self.lower_freq_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_freq_filter_btn.isChecked():
            if not signal_freqs[0] < filters_ok(self.upper_freq_spinbox,
                                                self.upper_freq_filter_unit,
                                                self.upper_freq_confidence):
                upper_limit_ok = False
        if any_checked:
            return band_filter_ok and lower_limit_ok and upper_limit_ok
        else:
            return lower_limit_ok and upper_limit_ok

    def band_filters_ok(self, signal_name):
        if not self.apply_remove_band_filter_btn.isChecked():
            return True
        undef_band = is_undef_band(self.db.loc[signal_name])
        if undef_band:
            if self.include_undef_bands.isChecked():
                return True
            else:
                return False

        signal_bands = (int(self.db.at[signal_name, Signal.INF_BAND]),
                        int(self.db.at[signal_name, Signal.SUP_BAND]))

        lower_limit_ok = True
        upper_limit_ok = True
        if self.activate_low_band_filter_btn.isChecked():
            if not signal_bands[1] >= filters_ok(self.lower_band_spinbox,
                                                 self.lower_band_filter_unit,
                                                 self.lower_band_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_band_filter_btn.isChecked():
            if not signal_bands[0] < filters_ok(self.upper_band_spinbox,
                                                self.upper_band_filter_unit,
                                                self.upper_band_confidence):
                upper_limit_ok = False
        return lower_limit_ok and upper_limit_ok

    def category_filters_ok(self, signal_name):
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
        parents = [item for item in selected_items_text if item in Constants.MODES.keys()]
        children = [item for item in selected_items_text if item not in parents]
        ok = []
        for item in selected_items:
            if item.text(0) in parents:
                ok.append(item.text(0) in signal_mode)
            elif not item.parent().isSelected():
                ok.append(item.text(0) == signal_mode)
        return any(ok)

    def modulation_filters_ok(self, signal_name):
        if not self.apply_remove_modulation_filter_btn.isChecked():
            return True
        signal_modulation = self.db.at[signal_name, Signal.MODULATION]
        for item in self.modulation_list.selectedItems():
            if item.text() == signal_modulation:
                return True
        return False

    def location_filters_ok(self, signal_name):
        if not self.apply_remove_location_filter_btn.isChecked():
            return True
        signal_location = self.db.at[signal_name, Signal.LOCATION]
        for item in self.locations_list.selectedItems():
            if item.text() == signal_location:
                return True
        return False

    def acf_filters_ok(self, signal_name):
        if not self.apply_remove_acf_filter_btn.isChecked():
            return True
        signal_acf = self.db.at[signal_name, Signal.ACF]
        if signal_acf == Constants.UNKNOWN:
            if self.include_undef_acf.isChecked():
                return True
            else:
                return False
        else:
            signal_acf = float(signal_acf.rstrip("ms"))
            tolerance = self.acf_spinbox.value() * self.acf_confidence.value() / 100
            upper_limit = self.acf_spinbox.value() + tolerance
            lower_limit = self.acf_spinbox.value() - tolerance
            if signal_acf <= upper_limit and signal_acf >= lower_limit:
                return True
            else:
                return False

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def display_specs(self, item, previous_item):
        self.display_spectrogram()
        if item:
            self.current_signal_name = item.text()
            self.name_lab.setText(self.current_signal_name)
            self.name_lab.setAlignment(Qt.AlignHCenter)
            current_signal = self.db.loc[self.current_signal_name]
            self.url_button.setEnabled(True)
            if not current_signal.at[Signal.WIKI_CLICKED]:
                self.url_button.setStyleSheet(f"color: {self.url_button.colors.active};")
            else:
                self.url_button.setStyleSheet(f"color: {self.url_button.colors.clicked};")
            category_code = current_signal.at[Signal.CATEGORY_CODE]
            undef_freq = is_undef_freq(current_signal)
            undef_band = is_undef_band(current_signal)
            if not undef_freq:
                self.freq_lab.setText(format_numbers(current_signal.at[Signal.INF_FREQ],
                                                     current_signal.at[Signal.SUP_FREQ])
                )
            else:
                self.freq_lab.setText("Undefined")
            if not undef_band:
                self.band_lab.setText(format_numbers(current_signal.at[Signal.INF_BAND],
                                                     current_signal.at[Signal.SUP_BAND])
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
            self.url_button.setStyleSheet(f"color: {self.url_button.colors.inactive};")
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
        default_pic = os.path.join(self.default_images_folder, Constants.NOT_SELECTED)
        item = self.result_list.currentItem()
        if item:
            spectrogram_name = item.text()
            path_spectr = os.path.join(Constants.DATA_FOLDER,
                                       Constants.SPECTRA_FOLDER,
                                       spectrogram_name + Constants.SPECTRA_EXT)
            if not QFileInfo(path_spectr).exists():
                path_spectr = os.path.join(self.default_images_folder, Constants.NOT_AVAILABLE)
        else:
            path_spectr = default_pic
        self.spectrogram.setPixmap(QPixmap(path_spectr))

    def activate_band_category(self, band_label, activate = True):
        color = self.active_color if activate else self.inactive_color
        for label in band_label:
            label.setStyleSheet(f"color: {color};")

    def set_band_range(self, current_signal = None):
        if current_signal is not None and not is_undef_freq(current_signal):
            lower_freq = int(current_signal.at[Signal.INF_FREQ])
            upper_freq = int(current_signal.at[Signal.SUP_FREQ])
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
        self.reset_frequency_filters_btn.clicked.emit()
        self.reset_band_filters_btn.clicked.emit()
        self.reset_cat_filters_btn.clicked.emit()
        self.reset_mode_filters_btn.clicked.emit()
        self.reset_modulation_filters_btn.clicked.emit()
        self.reset_location_filters_btn.clicked.emit()
        self.reset_acf_filters_btn.clicked.emit()

    @pyqtSlot()
    def go_to_web_page_signal(self):
        if self.current_signal_name:
            self.url_button.setStyleSheet(f"color: {self.url_button.colors.clicked}")
            webbrowser.open(self.db.at[self.current_signal_name, Signal.URL])
            self.db.at[self.current_signal_name, Signal.WIKI_CLICKED] = True

    def closeEvent(self, event):
        if self.download_window.isVisible():
            self.download_window.close()
        super().closeEvent(event)


if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    img = QPixmap(":/icons/Artemis3.500px.png")
    # img = img.scaled(600, 600, aspectRatioMode = Qt.KeepAspectRatio)
    # splash = QSplashScreen(img)
    # splash.show()
    # sleep(2)
    w = Artemis()
    # splash.finish(w)
    sys.exit(my_app.exec_())
