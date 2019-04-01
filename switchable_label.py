from PyQt5.QtWidgets import QLabel

class SwitchableLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.switch_on_color = None
        self.switch_off_color = None

    def set_colors(self, on, off):
        self.switch_on_color = on
        self.switch_off_color = off

    def switch_on(self):
        self.setStyleSheet(f"""background-color: {self.switch_on_color};
        color:#000000;""")

    def switch_off(self):
        self.setStyleSheet(f"""background-color: {self.switch_off_color};
        color:#000000;""")


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
