import sys
import os
from pandas import read_csv
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMessageBox,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QFileInfo

qt_creator_file = "main_window.ui"

Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.load_db()
        self.display_signals()
        self.search_bar.textChanged.connect(self.display_signals)
        self.result_list.itemSelectionChanged.connect(self.display_spectrogram)

    def load_db(self):
        try:
            db = read_csv(os.path.join('Data', 'db.csv'), 
                      sep = '*',
                      header = None,
                      prefix = 'signal_')
        except FileNotFoundError:
            self.signal_names = ''
            self.search_bar.setDisabled(True)
            box = QMessageBox(self)
            box.setStyleSheet("""
                color:#FFFFFF;
            """)
            box.setWindowTitle("No database")
            box.setText("No database available.\n"
                "Go to Updates->Download database.")
            box.show()
        else:
            self.signal_names = db['signal_0']

    def display_signals(self):
        self.result_list.clear()
        for signal in self.signal_names:
            if self.search_bar.text().lower() in signal.lower():
                self.result_list.addItem(signal)

    def display_spectrogram(self):
        spectrogram_name = self.result_list.currentItem().text()
        path_spectr = os.path.join("Data", "Spectra", spectrogram_name + ".jpg")
        if not QFileInfo(path_spectr).exists():
            path_spectr = os.path.join("icons_imgs", "image_not_found.png")
        self.spectrogram.setPixmap(QPixmap(path_spectr))


if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    sys.exit(my_app.exec_())