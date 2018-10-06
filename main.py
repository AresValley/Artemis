import sys
import os
import webbrowser
from collections import namedtuple

from pandas import read_csv
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMessageBox,
                             qApp,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QFileInfo, QSize

from audio_player import AudioPlayer

qt_creator_file = "main_window.ui"

Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)

class MyApp(QMainWindow, Ui_MainWindow):
    Band = namedtuple("Band", ["lower", "upper"])
    ELF =  Band(3, 30)
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

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.actionExit.triggered.connect(qApp.quit)
        self.db_version = None
        self.db = None
        self.current_signal_name = ''
        self.undefined_freq = False
        self.undefined_band = False
        self.signal_names = []
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

        self.property_labels = [self.name_lab,
                                self.freq_lab,
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
                               names = names,
                               )
        except FileNotFoundError:
            self.search_bar.setDisabled(True)
            box = QMessageBox(self)
            box.setWindowTitle("No database")
            box.setText("No database available.\n"
                "Go to Updates->Download database.")
            box.show()
        else:
            self.signal_names = self.db.index
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
            self.setStatusTip("Database version: undefined.")
        else:
            self.setStatusTip(f"Database version: {self.db_version}")

    def display_signals(self):
        self.result_list.clear()
        for signal in self.signal_names:
            if self.search_bar.text().lower() in signal.lower():
                self.result_list.addItem(signal)

    def display_specs(self):
        self.display_spectrogram()
        item = self.result_list.currentItem()
        if item:
            self.current_signal_name = item.text()
            words = self.current_signal_name.split(' ')
            if len(words) > 3:
                words_per_row = len(words) // 2
                words = ' '.join(words[:words_per_row]) \
                    + "\n" + ' '.join(words[words_per_row:])
            else:
                words = self.current_signal_name
            self.name_lab.setText(words)
            current_signal = self.db.loc[self.current_signal_name]
            self.url_button.setEnabled(True)
            self.url_button.setStyleSheet("color: #4c75ff;")
            category_code = current_signal.loc["category_code"]
            self.find_if_undefined(current_signal)
            if not self.undefined_freq:
                self.freq_lab.setText(self.format_numbers(
                                          current_signal.loc["inf_freq"],
                                          current_signal.loc["sup_freq"])
                                     )
            else:
                self.freq_lab.setText("Undefined")
            if not self.undefined_band:
                self.band_lab.setText(self.format_numbers(
                                        current_signal.loc["inf_band"],
                                        current_signal.loc["sup_band"])
                                     )
            else:
                self.band_lab.setText("Undefined")

            self.mode_lab.setText(current_signal.loc["mode"])
            self.modul_lab.setText(current_signal.loc["modulation"])
            self.loc_lab.setText(current_signal.loc["location"])
            self.acf_lab.setText(current_signal.loc["acf"])
            self.description_text.setText(current_signal.loc["description"])
            for cat, cat_lab in zip(category_code, self.category_labels):
                if cat == '0':
                    cat_lab.setStyleSheet("color: #9f9f9f;")
                elif cat == '1':
                    cat_lab.setStyleSheet("color: #39eaff;")
            self.set_band_range(current_signal)
            self.audio_widget.set_audio_player(self.current_signal_name)
        else:
            self.url_button.setEnabled(False)
            self.url_button.setStyleSheet("color: #898989;")
            self.current_signal_name = ''
            for lab in self.property_labels:
                lab.setText("N/A")
            for lab in self.category_labels:
                lab.setStyleSheet("""color: #9f9f9f;""")
            self.set_band_range()
            self.audio_widget.set_audio_player()

    def find_if_undefined(self, current_signal):
        lower_freq = current_signal.loc["inf_freq"]
        lower_band = current_signal.loc["inf_band"]
        upper_freq = current_signal.loc["sup_freq"]
        upper_band = current_signal.loc["sup_band"]
        if lower_freq == '0' and upper_freq == "100000000000":
            self.undefined_freq = True
        else:
            self.undefined_freq = False
        if lower_band == '0' and upper_band == '100000000':
            self.undefined_band = True
        else:
            self.undefined_band = False

    @classmethod
    def format_numbers(cls, lower, upper):
        units = {1: 'Hz', 1000: 'kHz', 10**6: 'MHz', 10**9: 'GHz'}
        lower_factor = cls.change_unit(lower)
        upper_factor = cls.change_unit(upper)
        pre_lower = lower
        pre_upper = upper
        lower = int(lower) / lower_factor
        upper = int(upper) / upper_factor
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
        default_pic = os.path.join("icons_imgs", "image_not_found.png")
        item = self.result_list.currentItem()
        if item:
            spectrogram_name = item.text()
            path_spectr = os.path.join("Data", "Spectra", spectrogram_name + ".jpg")
            if not QFileInfo(path_spectr).exists():
                path_spectr = default_pic
        else:
            path_spectr = default_pic
        self.spectrogram.setPixmap(QPixmap(path_spectr))

    @staticmethod
    def activate_band_category(band_label, activate = True):
        color = "#39eaff;" if activate else "#9f9f9f"
        for label in band_label:
            label.setStyleSheet(f"color: {color}")

    def set_band_range(self, current_signal = None):
        if current_signal is not None and not self.undefined_freq:
            lower_freq = int(current_signal.loc["inf_freq"])
            upper_freq = int(current_signal.loc["sup_freq"])
            zipped = zip(self.bands, self.band_labels)
            for i, w in enumerate(zipped):
                band, band_label = w
                if lower_freq >= band.lower and lower_freq < band.upper:
                    self.activate_band_category(band_label)
                    for uband, uband_label in list(zipped)[i + 1:]:
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

    def go_to_web_page_signal(self):
        if self.current_signal_name:
            self.url_button.setStyleSheet("color: #942ccc;")
            webbrowser.open(self.db.loc[self.current_signal_name].loc["url"])
            # self.db.loc[self.current_signal_name].loc["url_clicked"] = True



if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    sys.exit(my_app.exec_())