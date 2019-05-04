from PyQt5.QtWidgets import QLabel
from constants import ForecastColors


class _BaseSwitchableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_on = False

    def switch_on(self):
        self.is_on = True

    def switch_off(self):
        self.is_on = False


class SwitchableLabel(_BaseSwitchableLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.switch_on_colors = ()
        self.switch_off_colors = ()
        self.text_color = ''

    def switch_on(self):
        super().switch_on()
        self.__apply_colors(*self.switch_on_colors)

    def switch_off(self):
        super().switch_off()
        self.__apply_colors(*self.switch_off_colors)

    def __apply_colors(self, start, end):
        self.setStyleSheet(
            f"""
            color:{self.text_color};
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,stop:0 {start} ,stop: 1 {end});
            """
        )


class SingleColorSwitchableLabel(_BaseSwitchableLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_color = ForecastColors.WARNING_COLOR

    def switch_on(self):
        super().switch_on()
        self.setStyleSheet(f"background-color: {self.active_color};")

    def switch_off(self):
        super().switch_off()
        self.setStyleSheet("background-color: transparent;")


class MultiColorSwitchableLabel(_BaseSwitchableLabel):

    LEVEL_COLORS = {
        9: ForecastColors.KP9_COLOR,
        8: ForecastColors.KP8_COLOR,
        7: ForecastColors.KP7_COLOR,
        6: ForecastColors.KP6_COLOR,
        5: ForecastColors.KP5_COLOR
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 0

    def switch_on(self):
        if 5 <= self.level <= 9:
            super().switch_on()
            self.setStyleSheet(f"""
            background-color: {self.LEVEL_COLORS[self.level]};
            """)

    def switch_off(self):
        super().switch_off()
        self.setStyleSheet("background-color: transparent;")


class SwitchableLabelsIterable:
    def __init__(self, *labels):
        self.labels = labels

    def __iter__(self):
        for lab in self.labels:
            yield lab

    def switch_on(self, label):
        for lab in self.labels:
            if lab is label:
                lab.switch_on()
            else:
                lab.switch_off()

    def switch_off_all(self):
        for lab in self.labels:
            lab.switch_off()

    def set(self, attr, value):
        for lab in self.labels:
            setattr(lab, attr, value)

    def refresh(self):
        for lab in self.labels:
            if lab.is_on:
                lab.switch_on()
            else:
                lab.switch_off()
