from PyQt5.QtWidgets import QLabel
from constants import ForecastColors


class _BaseSwitchableLabel(QLabel):
    """Subclass QLabel. Base class for the switchable labels."""

    def __init__(self, parent=None):
        """Set is_on = False and level = 0."""
        super().__init__(parent)
        self.is_on = False
        self.level = 0

    def switch_on(self):
        """Set is_on = True."""
        self.is_on = True

    def switch_off(self):
        """Set is_on = False."""
        self.is_on = False


class SwitchableLabel(_BaseSwitchableLabel):
    """Subclass _BaseSwitchableLabel."""

    def __init__(self, parent=None):
        """Define text and colors attributes."""
        super().__init__(parent)
        self.switch_on_colors = ()
        self.switch_off_colors = ()
        self.text_color = ''

    def switch_on(self):
        """Extend _BaseSwitchableLabel.switch_on.

        Apply the active state colors."""
        super().switch_on()
        self.__apply_colors(*self.switch_on_colors)

    def switch_off(self):
        """Extend _BaseSwitchableLabel.switch_off.

        Apply the inactive state colors."""
        super().switch_off()
        self.__apply_colors(*self.switch_off_colors)

    def __apply_colors(self, start, end):
        """Set text and background color of the label."""
        self.setStyleSheet(
            f"""
            color:{self.text_color};
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,stop:0 {start} ,stop: 1 {end});
            """
        )


class SingleColorSwitchableLabel(_BaseSwitchableLabel):
    """Subclass _BaseSwitchableLabel."""

    THRESHOLD = 30

    def __init__(self, parent=None):
        """Set default active color."""
        super().__init__(parent)
        self.active_color = ForecastColors.WARNING_COLOR

    def switch_on(self):
        """Extend _BaseSwitchableLabel.switch_on.

        Apply the active state color if level >= THRESHOLD."""
        if self.level >= self.THRESHOLD:
            super().switch_on()
            self.setStyleSheet(f"color: {self.active_color}")

    def switch_off(self):
        """Extend _BaseSwitchableLabel.switch_off.

        Apply an empty stylesheet."""
        super().switch_off()
        self.setStyleSheet("")


class MultiColorSwitchableLabel(_BaseSwitchableLabel):
    """Subclass _BaseSwitchableLabel."""

    LEVEL_COLORS = {
        9: ForecastColors.KP9_COLOR,
        8: ForecastColors.KP8_COLOR,
        7: ForecastColors.KP7_COLOR,
        6: ForecastColors.KP6_COLOR,
        5: ForecastColors.KP5_COLOR
    }

    MIN_LEVEL = list(LEVEL_COLORS.keys())[-1]
    MAX_LEVEL = list(LEVEL_COLORS.keys())[0]

    def __init__(self, parent=None):
        """Initialize the instance."""
        super().__init__(parent)

    def switch_on(self):
        """Extend _BaseSwitchableLabel.switch_on.

        Apply the active state color based on LEVEL_COLORS."""
        if self.MIN_LEVEL <= self.level <= self.MAX_LEVEL:
            super().switch_on()
            self.setStyleSheet(
                f"""color: {self.LEVEL_COLORS[self.level]};
                text-decoration: underline;"""
            )

    def switch_off(self):
        """Extend _BaseSwitchableLabel.switch_off.

        Apply an empty stylesheet."""
        super().switch_off()
        self.setStyleSheet("")


class SwitchableLabelsIterable:
    """Iterable class of _BaseSwitchableLabel."""

    def __init__(self, *labels):
        """Set the labels to iterate through."""
        self.labels = labels

    def __iter__(self):
        """Define the iterator."""
        for lab in self.labels:
            yield lab

    def switch_on(self, label):
        """Switch on the label 'label. Switch off all the other labels."""
        for lab in self.labels:
            if lab is label:
                lab.switch_on()
            else:
                lab.switch_off()

    def switch_off_all(self):
        """Switch off all the labels."""
        for lab in self.labels:
            lab.switch_off()

    def set(self, attr, value):
        """Set the attribute 'attr' equal to 'value' for all the labels."""
        for lab in self.labels:
            setattr(lab, attr, value)

    def refresh(self):
        """Refresh the state of all the labels.

        Used after theme has changed."""
        for lab in self.labels:
            if lab.is_on:
                lab.switch_on()
            else:
                lab.switch_off()
