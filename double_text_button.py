from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot

class DoubleTextButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.clicked.connect(self.__manage_click)

    def set_texts(self, text_a, text_b):
        self.__text_a = text_a
        self.__text_b = text_b

    def set_slave_filters(self, simple_ones, 
                          radio_1 = None,
                          ruled_by_radio_1 = None, 
                          radio_2 = None,
                          ruled_by_radio_2 = None):
        self.__simple_ones = simple_ones
        self.__ruled_by_radio_1 = ruled_by_radio_1
        self.__radio_1 = radio_1
        self.__ruled_by_radio_2 = ruled_by_radio_2
        self.__radio_2 = radio_2

    @pyqtSlot()
    def __manage_click(self):
        if self.isChecked():
            self.setText(self.__text_b)
            enable = False
        else:
            self.setText(self.__text_a)
            enable = True
        for f in self.__simple_ones:
            f.setEnabled(enable)
        radio_btns = self.__radio_1, self.__radio_2
        ruled_widgets = self.__ruled_by_radio_1, self.__ruled_by_radio_2
        for radio_btn, ruled_by in zip(radio_btns, ruled_widgets):
            if ruled_by:
                for f in ruled_by:
                    if radio_btn.isChecked():
                        f.setEnabled(enable)
                    else:
                        f.setEnabled(False)
