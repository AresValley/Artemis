import sys
import os
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

qt_creator_file = "main_window.ui"

Ui_MainWindow, _ = uic.loadUiType(qt_creator_file)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(my_app.exec_())