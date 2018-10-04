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

        self.band_labels = [
            [self.elf, self.elf_s1, self.elf_s2],
            [self.slf, self.slf_s1, self.slf_s2],
            [self.ulf, self.ulf_s1, self.ulf_s2],
            [self.vlf, self.vlf_s1, self.vlf_s2],
            [self.lf , self.lf_s1 , self.lf_s2],
            [self.mf , self.mf_s1 , self.mf_s2],
            [self.hf , self.hf_s1 , self.hf_s2],
            [self.vhf, self.vhf_s1, self.vhf_s2],
            [self.uhf, self.uhf_s1, self.uhf_s2],
            [self.shf, self.shf_s1, self.shf_s2],
            [self.ehf, None,        None],
        ]

    def load_db(self):
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
                                        "acf",],
                               )
            self.db.fillna("N/A", inplace = True)
        except FileNotFoundError:
            self.search_bar.setDisabled(True)
            box = QMessageBox(self)
            box.setWindowTitle("No database")
            box.setText("No database available.\n"
                "Go to Updates->Download database.")
            box.show()
        else:
            self.signal_names = self.db.index
        
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
            self.url_button.setEnabled(True)
            self.url_button.setStyleSheet("color: #4c75ff;")
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
            print(current_signal.loc["inf_band"], current_signal.loc["sup_band"])
            category_code = current_signal.loc["category_code"]
            self.freq_lab.setText(self.format_numbers(
                                    current_signal.loc["inf_freq"],
                                    current_signal.loc["sup_freq"])
                                 )
            self.band_lab.setText(self.format_numbers(
                                    current_signal.loc["inf_band"],
                                    current_signal.loc["sup_band"])
                                 )
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

    @classmethod
    def format_numbers(cls, lower, upper):
        units = {1: 'Hz', 1000: 'kHz', 10**6: 'MHz', 10**9: 'GHz'}
        lower_factor = cls.change_unit(lower)
        upper_factor = cls.change_unit(upper)
        if lower != upper:
            lower = int(lower) / lower_factor
            upper = int(upper) / upper_factor
            return f"{lower} {units[lower_factor]} - {upper} {units[upper_factor]}"
        else:
            lower = int(lower) / lower_factor
            return f"{lower} {units[lower_factor]}"

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

    def set_band_range(self, current_signal = None):
        # How to deal with one-frequency signals?
        if current_signal is not None:
            inf_band = int(current_signal.loc["inf_freq"])
            sup_band = int(current_signal.loc["sup_freq"])
            for band, band_label in zip(self.bands, self.band_labels):
                delta = (band.upper - band.lower) // 2 + band.lower
                if inf_band <= band.lower and sup_band > band.lower:
                    band_label[0].setStyleSheet("color: #39eaff;")
                else:
                    band_label[0].setStyleSheet("color: #9f9f9f;")
                if band_label[1]:
                    if inf_band <= delta and sup_band >= delta:
                        band_label[1].setStyleSheet("color: #39eaff;")
                    else:
                        band_label[1].setStyleSheet("color: #9f9f9f;")
                if band_label[2]:                
                    if inf_band <= band.upper and sup_band > band.upper:
                        band_label[2].setStyleSheet("color: #39eaff;")
                    else:
                        band_label[2].setStyleSheet("color: #9f9f9f;")
        else:
            [label.setStyleSheet("color: #9f9f9f;") for labels in self.band_labels for label in labels if label]

    def go_to_web_page_signal(self):
        if self.current_signal_name:
            webbrowser.open(self.db.loc[self.current_signal_name].loc["url"])



if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    sys.exit(my_app.exec_())