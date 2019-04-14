from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize

class FixedAspectRatioWidget(QWidget):
    space = 10
    def __init__(self, parent = None):
        super().__init__(parent)
        self.labels = []

    def resizeEvent(self, event):
        h, w = self.height(), self.width()
        h_lbl = h / 9 - self.space
        w_lbl = 5 * h_lbl

        if w_lbl > w:
            w_lbl = w
            h_lbl = h / 9 - self.space

        for label in self.labels:
            label.rescale(QSize(w_lbl, h_lbl))
