from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class FixedAspectRatioLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.pixmap = None

    def set_default_stylesheet(self):
        self.setStyleSheet("""border-width: 1px;
        border-style: solid;
        border-color: black;"""
        )

    def make_transparent(self):
        self.setText('')
        self.setStyleSheet("border-width: 0px;")

    def apply_pixmap(self):
        if self.pixmap:
            self.setPixmap(
                self.pixmap.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                )
            )

    def rescale(self, size):
        self.resize(size)
        self.apply_pixmap()
