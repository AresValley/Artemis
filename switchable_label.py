from PyQt5.QtWidgets import QLabel

class SwitchableLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.switch_on_colors = ()
        self.switch_off_colors = ()
        self.text_color = ''
        self.is_on = False

    def switch_on(self):
        self.is_on = True
        self.__apply_colors(*self.switch_on_colors)

    def switch_off(self):
        self.is_on = False
        self.__apply_colors(*self.switch_off_colors)

    def __apply_colors(self, start, end):
        self.setStyleSheet(
            f"""
            color:{self.text_color};
            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,stop:0 {start} ,stop: 1 {end});
            """
        )


class SwitchableLabelsIterable(object):
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
