from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot

class DoubleTextButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.clicked.connect(self.manage_click)

    def set_texts(self, text_a, text_b):
        self.text_a = text_a
        self.text_b = text_b

    def set_slave_filters(self, *filters):
        self.filters = filters

    @pyqtSlot()
    def manage_click(self):
        if self.isChecked():
            self.setText(self.text_b)
            enable = False
        else:
            self.setText(self.text_a)
            enable = True
        for f in self.filters:
            f.setEnabled(enable)
