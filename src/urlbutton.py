from PyQt5.QtWidgets import QPushButton
from collections import namedtuple
from enum import Enum, auto


class UrlButton(QPushButton):
    """Define the behaviour of the wiki button."""

    class State(Enum):
        """Possible states of the button."""
        ACTIVE = auto()
        INACTIVE = auto()
        CLICKED = auto()

    _UrlColors = namedtuple(
        "UrlColors",
        [
            "INACTIVE",
            "ACTIVE",
            "CLICKED",
            "ACTIVE_HOVER",
            "CLICKED_HOVER",
        ]
    )
    _COLORS = _UrlColors(
        "#9f9f9f",
        "#4c75ff",
        "#942ccc",
        "#808FFF",
        "#DE78FF",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_enabled(self, state):
        """Enable the button and set the stylesheet."""
        super().setEnabled(True)
        if state is self.State.ACTIVE:
            color = self._COLORS.ACTIVE
        else:
            color = self._COLORS.CLICKED
        self.setStyleSheet(f"""
            QPushButton {{
                border: 0px;
                background-color: transparent;
                color: {color};
            }}
            QPushButton::hover {{
                border: 0px;
                background-color: transparent;
                color: {self._COLORS.ACTIVE_HOVER};
            }}
        """)

    def set_disabled(self):
        """Disable the button and set the stylesheet."""
        super().setEnabled(False)
        self.setStyleSheet(f"""
            QPushButton:disabled {{
                border: 0px;
                background-color: transparent;
                color: {self._COLORS.INACTIVE};
            }}
        """)

    def set_clicked(self):
        """Apply the stylesheet for the clicked state."""
        self.setStyleSheet(f"""
            QPushButton {{
                border: 0px;
                background-color: transparent;
                color: {self._COLORS.CLICKED};
            }}
            QPushButton::hover {{
                border: 0px;
                background-color: transparent;
                color: {self._COLORS.CLICKED_HOVER};
            }}
        """)
