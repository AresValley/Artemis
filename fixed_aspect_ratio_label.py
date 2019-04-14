from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class FixedAspectRatioLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pixmap = None

    def set_default_stylesheet(self):
        self.setStyleSheet("""
            color: #ffffff;
            background-color: #666666;
        """)

    def make_transparent(self):
        self.setText('')
        self.setStyleSheet("background-color: transparent;")

    def apply_pixmap(self):
        if self.pixmap:
            self.setPixmap(
                self.pixmap.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

    def rescale(self, size):
        self.resize(size)
        self.apply_pixmap()
