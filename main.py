import sys
import os
from pandas import read_csv
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMessageBox,
                             qApp,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QFileInfo, QSize
import webbrowser

from audio_player import AudioPlayer

qt_creator_file = "main_window.ui"

Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)

class MyApp(QMainWindow, Ui_MainWindow):
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
            self.name_lab.setText(self.current_signal_name)
            current_signal = self.db.loc[self.current_signal_name]
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
            self.audio_widget.set_audio_player(self.current_signal_name)
        else:
            self.url_button.setEnabled(False)
            self.url_button.setStyleSheet("color: #898989;")
            self.current_signal_name = ''
            for lab in self.property_labels:
                lab.setText("N/A")
            for lab in self.category_labels:
                lab.setStyleSheet("""color: #9f9f9f;""")
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
        if len(num) < 4:
            return 1
        elif len(num) < 7:
            return 1000
        elif len(num) < 10:
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

    def go_to_web_page_signal(self):
        if self.current_signal_name:
            webbrowser.open(self.db.loc[self.current_signal_name].loc["url"])



if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    sys.exit(my_app.exec_())