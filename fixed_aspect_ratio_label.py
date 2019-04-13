from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize, Qt

class FixedAspectRatioLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pixmap = None

    def rescale(self, w, h):
        self.resize(QSize(w, h))
        if self.pixmap:
            self.setPixmap(
                self.pixmap.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
