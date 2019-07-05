from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot


class DoubleTextButton(QPushButton):
    """Subclass QPushButton.

    A click will deactivate/activate a series of 'slave' widgets depending
    on the 'checked' status of the button."""

    def __init__(self, parent=None):
        """Extends QPushButton.__init__."""
        super().__init__(parent)
        self.clicked.connect(self._manage_click)

    def set_texts(self, text_a, text_b):
        """Set the two texts to be displayed."""
        self._text_a = text_a
        self._text_b = text_b

    def set_slave_filters(self, simple_ones=None,
                          radio_1=None,
                          ruled_by_radio_1=None,
                          radio_2=None,
                          ruled_by_radio_2=None):
        """Set all the 'slave' widgets.

        Keyword arguments:
        simple_ones -- a list of widgets.
        radio_1 -- a radio button.
        ruled_by_radio_1 -- a list of widgets whose status depend upon radio_1.
        radio_2 -- a radio button.
        ruled_by_radio_2 -- a list of widgets whose status depend upon radio_2."""
        self._simple_ones = simple_ones
        self._ruled_by_radio_1 = ruled_by_radio_1
        self._radio_1 = radio_1
        self._ruled_by_radio_2 = ruled_by_radio_2
        self._radio_2 = radio_2

    @pyqtSlot()
    def _manage_click(self):
        """Set the status of all the 'slave widgets' based on the status of the instance."""
        if self.isChecked():
            self.setText(self._text_b)
            enable = False
        else:
            self.setText(self._text_a)
            enable = True
        for f in self._simple_ones:
            f.setEnabled(enable)
        radio_btns = self._radio_1, self._radio_2
        ruled_widgets = self._ruled_by_radio_1, self._ruled_by_radio_2
        for radio_btn, ruled_by in zip(radio_btns, ruled_widgets):
            if ruled_by:
                for f in ruled_by:
                    if radio_btn.isChecked():
                        f.setEnabled(enable)
                    else:
                        f.setEnabled(False)
