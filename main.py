from collections import namedtuple
from functools import partial
import webbrowser
import os
import sys

from pandas import read_csv
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMessageBox,
                             qApp,
                             QDesktopWidget,
                             QListWidgetItem,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QFileInfo, QSize, Qt, pyqtSlot

from audio_player import AudioPlayer

from double_text_button import DoubleTextButton

qt_creator_file = "main_window.ui"

Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)

class MyApp(QMainWindow, Ui_MainWindow):
    Band = namedtuple("Band", ["lower", "upper"])
    ELF = Band(0, 30) # Formally it is (3, 30) Hz.
    SLF = Band(30, 300)
    ULF = Band(300, 3000)
    VLF = Band(3000, 30000)
    LF  = Band(30 * 10**3, 300 * 10**3)
    MF  = Band(300 * 10 ** 3, 3000 * 10**3)
    HF  = Band(3 * 10**6, 30 * 10**6)
    VHF = Band(30 * 10**6, 300 * 10**6)
    UHF = Band(300 * 10**6, 3000 * 10**6)
    SHF = Band(3 * 10**9, 30 * 10**9)
    EHF = Band(30 * 10**9, 300 * 10**9)
    bands = ELF, SLF, ULF, VLF, LF, MF, HF, VHF, UHF, SHF, EHF
    active_color = "#39eaff"
    inactive_color = "#9f9f9f"
    conversion_factors = {"Hz":1, "kHz":1000, "MHz":1000000, "GHz":1000000000}

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_initial_size()
        self.show()
        self.actionExit.triggered.connect(qApp.quit)
        self.db_version = None
        self.db = None
        self.current_signal_name = ''
        self.signal_names = []
        self.total_signals = 0

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

        self.connect_to(
            objects_to_connect = {self.lower_freq_spinbox: 'valueChanged',
                                  self.upper_freq_spinbox: 'valueChanged',
                                  self.lower_freq_filter_unit: 'currentTextChanged',
                                  self.upper_freq_filter_unit: 'currentTextChanged',
                                  self.activate_low_freq_filter_btn: 'toggled'},
            fun_to_connect = self.set_min_value_upper_limit,
            fun_args = [self.lower_freq_filter_unit, 
                        self.lower_freq_spinbox, 
                        self.upper_freq_filter_unit, 
                        self.upper_freq_spinbox]
        )

        self.connect_to(
            objects_to_connect = {self.lower_freq_spinbox: 'valueChanged',
                                  self.upper_freq_spinbox: 'valueChanged',
                                  self.lower_freq_filter_unit: 'currentTextChanged',
                                  self.upper_freq_filter_unit: 'currentTextChanged',
                                  self.activate_low_freq_filter_btn: 'clicked',
                                  self.activate_up_freq_filter_btn: 'clicked',
                                  self.lower_freq_confidence: 'valueChanged',
                                  self.upper_freq_confidence: 'valueChanged'},
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

        self.apply_remove_freq_filter_btn.set_texts("Apply", "Remove")
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
        self.reset_frequency_filters_btn.clicked.connect(partial(self.reset_fb_filters, 'freq'))

        # Manage bandwidth filters.

        self.connect_to(
            objects_to_connect = {self.lower_band_spinbox: 'valueChanged',
                                  self.upper_band_spinbox: 'valueChanged',
                                  self.lower_band_filter_unit: 'currentTextChanged',
                                  self.upper_band_filter_unit: 'currentTextChanged',
                                  self.activate_low_band_filter_btn: 'toggled'},
            fun_to_connect = self.set_min_value_upper_limit,
            fun_args = [self.lower_band_filter_unit, 
                        self.lower_band_spinbox, 
                        self.upper_band_filter_unit, 
                        self.upper_band_spinbox]
        )

        self.connect_to(
            objects_to_connect = {self.lower_band_spinbox: 'valueChanged',
                                  self.upper_band_spinbox: 'valueChanged',
                                  self.lower_band_filter_unit: 'currentTextChanged',
                                  self.upper_band_filter_unit: 'currentTextChanged',
                                  self.activate_low_band_filter_btn: 'clicked',
                                  self.activate_up_band_filter_btn: 'clicked',
                                  self.lower_band_confidence: 'valueChanged',
                                  self.upper_band_confidence: 'valueChanged'},
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

        self.apply_remove_band_filter_btn.set_texts("Apply", "Remove")
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
        self.reset_band_filters_btn.clicked.connect(partial(self.reset_fb_filters, 'band'))

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

        self.apply_remove_cat_filter_btn.set_texts('Apply', 'Remove')   
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
        self.load_db()
        self.display_signals()
        self.search_bar.textChanged.connect(self.display_signals)
        self.result_list.currentItemChanged.connect(self.display_specs)
        self.audio_widget = AudioPlayer(self.play, 
                                        self.pause, 
                                        self.stop, 
                                        self.volume, 
                                        self.audio_progress)

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

    def load_db(self):
        names = ["name",
                 "inf_freq",
                 "sup_freq",
                 "mode",
                 "inf_band",
                 "sup_band",
                 "location",
                 "url",
                 "description",
                 "modulation",
                 "category_code",
                 "acf",]
        try:
            self.db = read_csv(os.path.join('Data', 'db.csv'), 
                               sep = '*',
                               header = None,
                               index_col = 0,
                               dtype = {'inf_freq': str,
                                        'sup_freq': str,
                                        'mode': str,
                                        'inf_band': str,
                                        'sup_band': str,
                                        'category_code': str,},
                               names = names,)
        except FileNotFoundError:
            self.search_bar.setDisabled(True)
            box = QMessageBox(self)
            box.setWindowTitle("No database")
            box.setText("No database available.\n"
                "Go to Updates->Download database.")
            box.show()
        else:
            self.signal_names = self.db.index
            self.total_signals = len(self.signal_names)
            self.db.fillna("N/A", inplace = True)
            self.db["url_clicked"] = False
            try:
                with open(os.path.join('Data', 'verdb.ini'), 'r') as dbver:
                    self.db_version = int(dbver.read())
            except (FileNotFoundError, ValueError):
                box = QMessageBox(self)
                box.setWindowTitle("No database version")
                box.setText("Unable to detect database version.\n"
                    "Possible data curruption.\n"
                    "Go to Updates->Force Download.")
                box.show()
                self.statusbar.setStyleSheet(f'color: {self.active_color}')
                self.statusbar.showMessage("Database version: undefined.")
            else:
                self.update_status_tip(self.total_signals)

    @staticmethod
    def connect_to(objects_to_connect, fun_to_connect, fun_args):
        for obj, signal in objects_to_connect.items():
            getattr(obj, signal).connect(
                partial(fun_to_connect, *fun_args)
            )

    @pyqtSlot()
    def set_min_value_upper_limit(self, lower_combo_box, 
                                  lower_spin_box, 
                                  upper_combo_box, 
                                  upper_spin_box):
        if lower_spin_box.isEnabled():
            unit_conversion = {'Hz' : ['kHz', 'MHz', 'GHz'],
                               'kHz': ['MHz', 'GHz'],
                               'MHz': ['GHz']
                              }
            lower_units = lower_combo_box.currentText()
            upper_units = upper_combo_box.currentText()
            lower_value = lower_spin_box.value()
            upper_value = upper_spin_box.value()
            inf_limit = (lower_value * self.conversion_factors[lower_units]) \
                // self.conversion_factors[upper_units]
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
            to_display += str(lower_spinbox.value()) + ' ' + lower_unit.currentText()
            activate_low = True
            color = self.active_color
            if lower_confidence.value() != 0:
                to_display += ' - ' + str(lower_confidence.value()) + ' %'
        else:
            to_display += 'DC'
        to_display += ' ÷ '
        if activate_up_btn.isChecked():
            to_display += str(upper_spinbox.value()) + ' ' + upper_unit.currentText()
            activate_high = True
            color = self.active_color
            if upper_confidence.value() != 0:
                to_display += ' + ' + str(upper_confidence.value()) + ' %'
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
    def activate_if_toggled(self, radio_btn, *widgets):
        toggled = True if radio_btn.isChecked() else False
        for w in widgets[:-1]: # Neglect the bool coming from the emitted signal.
            w.setEnabled(toggled)

    @pyqtSlot()
    def display_signals(self):
        self.result_list.clear()
        text = self.search_bar.text()
        available_signals = 0
        for signal in self.signal_names:
            if text.lower() in signal.lower()     and \
                self.frequency_filters_ok(signal) and \
                self.band_filters_ok(signal)      and \
                self.category_filters_ok(signal):
                self.result_list.addItem(signal)
                available_signals += 1
        self.update_status_tip(available_signals)

    def update_status_tip(self, available_signals):
        if available_signals < self.total_signals:
            self.statusbar.setStyleSheet(f'color: {self.active_color}')
        else:
            self.statusbar.setStyleSheet('color: #ffffff')
        self.statusbar.showMessage(f"{available_signals} out of {self.total_signals} signals displayed.")

    @pyqtSlot()
    def reset_fb_filters(self, ftype):
        if ftype != 'freq' and ftype != 'band':
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
        default_val = 1 if ftype == 'freq' else 5000
        if ftype == 'freq':
            for f in self.frequency_filters_btns:
                if f.isChecked():
                    f.setChecked(False)
        if apply_remove_btn.isChecked():
            apply_remove_btn.setChecked(False)
            apply_remove_btn.clicked.emit()
        if include_undef_btn.isChecked():
            include_undef_btn.setChecked(False)
        if activate_low.isChecked():
            activate_low.setChecked(False)
            activate_low.clicked.emit()
        if activate_up.isChecked():
            activate_up.setChecked(False)
            activate_up.clicked.emit()
        lower_unit.setCurrentText("MHz")
        upper_unit.setCurrentText("MHz")
        lower_spinbox.setValue(default_val)
        upper_spinbox.setMinimum(1)
        upper_spinbox.setValue(default_val)
        lower_confidence.setValue(0)
        upper_confidence.setValue(0)

    def reset_cat_filters(self):
        if self.apply_remove_cat_filter_btn.isChecked():
            self.apply_remove_cat_filter_btn.setChecked(False)
            self.apply_remove_cat_filter_btn.clicked.emit()
        for f in self.cat_filter_btns:
            f.setChecked(False) if f.isChecked() else None
        self.cat_at_least_one.setChecked(True)

    def frequency_filters_ok(self, signal_name):
        if not self.apply_remove_freq_filter_btn.isChecked():
            return True
        undef_freq, _ = self.find_if_undefined(self.db.loc[signal_name])
        if undef_freq:
            if self.include_undef_freqs.isChecked():
                return True
            else:
                return False

        signal_freqs = (int(self.db.at[signal_name, "inf_freq"]), 
                        int(self.db.at[signal_name, "sup_freq"]))

        band_filter_ok = False
        any_checked = False
        for btn, band_limits in zip(self.frequency_filters_btns, self.bands):
            if btn.isChecked():
                any_checked = True
                if signal_freqs[0] < band_limits.upper and signal_freqs[1] >= band_limits.lower:
                    band_filter_ok = True
        lower_limit_ok = True
        upper_limit_ok = True
        if self.activate_low_freq_filter_btn.isChecked():
            if not signal_freqs[1] >= self.filters_ok(self.lower_freq_spinbox, 
                                                      self.lower_freq_filter_unit,
                                                      self.lower_freq_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_freq_filter_btn.isChecked():
            if not signal_freqs[0] < self.filters_ok(self.upper_freq_spinbox, 
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
        _, undef_band = self.find_if_undefined(self.db.loc[signal_name])
        if undef_band:
            if self.include_undef_bands.isChecked():
                return True
            else:
                return False

        signal_bands = (int(self.db.at[signal_name, "inf_band"]), 
                        int(self.db.at[signal_name, "sup_band"]))

        lower_limit_ok = True
        upper_limit_ok = True
        if self.activate_low_band_filter_btn.isChecked():
            if not signal_bands[1] >= self.filters_ok(self.lower_band_spinbox, 
                                                      self.lower_band_filter_unit,
                                                      self.lower_band_confidence, -1):
                lower_limit_ok = False
        if self.activate_up_band_filter_btn.isChecked():
            if not signal_bands[0] < self.filters_ok(self.upper_band_spinbox, 
                                                     self.upper_band_filter_unit,
                                                     self.upper_band_confidence):
                upper_limit_ok = False
        return lower_limit_ok and upper_limit_ok

    def category_filters_ok(self, signal_name):
        if not self.apply_remove_cat_filter_btn.isChecked():
            return True
        cat_code = self.db.at[signal_name, 'category_code']
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

    @classmethod
    def filters_ok(cls, spinbox, filter_unit, confidence, sign = 1):
        band_filter = spinbox.value() * cls.conversion_factors[filter_unit.currentText()]
        return band_filter + sign * (confidence.value() * band_filter) // 100

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def display_specs(self, item, previous_item):
        self.display_spectrogram()
        if item:
            self.current_signal_name = item.text()
            self.name_lab.setText(self.current_signal_name)
            self.name_lab.setAlignment(Qt.AlignHCenter)
            current_signal = self.db.loc[self.current_signal_name]
            self.url_button.setEnabled(True)
            if not current_signal.at["url_clicked"]:
                self.url_button.setStyleSheet(f"color: {self.url_button.colors.active};")
            else:
                self.url_button.setStyleSheet(f"color: {self.url_button.colors.clicked};")
            category_code = current_signal.at["category_code"]
            undef_freq, undef_band = self.find_if_undefined(current_signal)
            if not undef_freq:
                self.freq_lab.setText(self.format_numbers(
                                      current_signal.at["inf_freq"],
                                      current_signal.at["sup_freq"])
                )
            else:
                self.freq_lab.setText("Undefined")
            if not undef_band:
                self.band_lab.setText(self.format_numbers(
                                      current_signal.at["inf_band"],
                                      current_signal.at["sup_band"])
                )
            else:
                self.band_lab.setText("Undefined")

            self.mode_lab.setText(current_signal.at["mode"])
            self.modul_lab.setText(current_signal.at["modulation"])
            self.loc_lab.setText(current_signal.at["location"])
            self.acf_lab.setText(current_signal.at["acf"])
            self.description_text.setText(current_signal.at["description"])
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
            self.name_lab.setText("No signal")
            self.name_lab.setAlignment(Qt.AlignHCenter)
            for lab in self.property_labels:
                lab.setText("N/A")
            for lab in self.category_labels:
                lab.setStyleSheet(f"color: {self.inactive_color};")
            self.set_band_range()
            self.audio_widget.set_audio_player()

    @staticmethod
    def find_if_undefined(current_signal):
        lower_freq = current_signal.at["inf_freq"]
        lower_band = current_signal.at["inf_band"]
        upper_freq = current_signal.at["sup_freq"]
        upper_band = current_signal.at["sup_band"]
        if lower_freq == '0' and upper_freq == "100000000000":
            undefined_freq = True
        else:
            undefined_freq = False
        if lower_band == '0' and upper_band == '100000000':
            undefined_band = True
        else:
            undefined_band = False
        return undefined_freq, undefined_band

    @classmethod
    def format_numbers(cls, lower, upper):
        units = {1: 'Hz', 1000: 'kHz', 10**6: 'MHz', 10**9: 'GHz'}
        lower_factor = cls.change_unit(lower)
        upper_factor = cls.change_unit(upper)
        pre_lower = lower
        pre_upper = upper
        lower = int(lower) / lower_factor
        upper = int(upper) / upper_factor
        if lower.is_integer():
            lower = int(lower)
        if upper.is_integer():
            upper = int(upper)
        if pre_lower != pre_upper:    
            return f"{lower:,} {units[lower_factor]} - {upper:,} {units[upper_factor]}"
        else:
            return f"{lower:,} {units[lower_factor]}"

    @staticmethod
    def change_unit(num):
        digits = len(num)
        if digits < 4:
            return 1
        elif digits < 7:
            return 1000
        elif digits < 10:
            return 10**6
        else:
            return 10**9
        
    def display_spectrogram(self):
        default_pic = os.path.join("icons_imgs", "nosignalselected.png")
        item = self.result_list.currentItem()
        if item:
            spectrogram_name = item.text()
            path_spectr = os.path.join("Data", "Spectra", spectrogram_name + ".jpg")
            if not QFileInfo(path_spectr).exists():
                path_spectr = os.path.join("icons_imgs", "spectrumnotavailable.png")
        else:
            path_spectr = default_pic
        self.spectrogram.setPixmap(QPixmap(path_spectr))

    @classmethod
    def activate_band_category(cls, band_label, activate = True):
        color = cls.active_color if activate else cls.inactive_color
        for label in band_label:
            label.setStyleSheet(f"color: {color};")

    def set_band_range(self, current_signal = None):
        if current_signal is not None and not self.find_if_undefined(current_signal)[0]:
            lower_freq = int(current_signal.at["inf_freq"])
            upper_freq = int(current_signal.at["sup_freq"])
            zipped = list(zip(self.bands, self.band_labels))
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

    @pyqtSlot()
    def go_to_web_page_signal(self):
        if self.current_signal_name:
            self.url_button.setStyleSheet(f"color: {self.url_button.colors.clicked}")
            webbrowser.open(self.db.at[self.current_signal_name, "url"])
            self.db.at[self.current_signal_name, "url_clicked"] = True



if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    sys.exit(my_app.exec_())