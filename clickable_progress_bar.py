from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt, pyqtSignal
from constants import Constants


class ClickableProgressBar(QProgressBar):
    """Subclass QProgressBar. Clickable progress bar class."""

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the instance."""
        self._text = ''
        super().__init__(parent)

    def text(self):
        """Return the text displayed on the bar."""
        return self._text

    def set_idle(self):
        """Set the bar to a non-downloading status."""
        self._text = Constants.CLICK_TO_UPDATE_STR
        self.setMaximum(self.minimum() + 1)

    def set_updating(self):
        """Set the bar to a downloading status."""
        self._text = Constants.UPDATING_STR
        self.setMaximum(self.minimum())

    def mousePressEvent(self, event):
        """Override QWidget.mousePressEvent. Detect a click on the bar."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)
