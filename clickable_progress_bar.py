from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt, pyqtSignal
from constants import Constants

class ClickableProgressBar(QProgressBar):

    clicked = pyqtSignal()

    def __init__(self, parent = None):
        self.__text = ''
        super().__init__(parent)

    def __set_text(self, text):
        self.__text = text

    def text(self):
        return self.__text

    def set_idle(self):
        self.__set_text(Constants.CLICK_TO_UPDATE_STR)
        self.setMaximum(self.minimum() + 1)

    def set_updating(self):
        self.__set_text(Constants.UPDATING_STR)
        self.setMaximum(self.minimum())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)
