from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class FixedAspectRatioLabel(QLabel):
    """Subclass QLabel. A resizable label class."""

    def __init__(self, parent=None):
        """Initialize the instance. Set the pixmap to None."""
        super().__init__(parent)
        self.pixmap = None

    def set_default_stylesheet(self):
        """Set the initial stylesheet of the label."""
        self.setStyleSheet("""border-width: 1px;
        border-style: solid;
        border-color: black;""")

    def make_transparent(self):
        """Make the label transparent.

        Remove text and border."""
        self.setText('')
        self.setStyleSheet("border-width: 0px;")

    def apply_pixmap(self):
        """Apply a scaled pixmap without modifying the dimension of the original one."""
        if self.pixmap:
            self.setPixmap(
                self.pixmap.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
                )
            )

    def rescale(self, size):
        """Rescale the widget and the displayed pixmap to the given size."""
        self.resize(size)
        self.apply_pixmap()
