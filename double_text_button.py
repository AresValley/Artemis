from PyQt5.QtWidgets import QPushButton

class DoubleTextButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.clicked.connect(self.change_text)

    def set_texts(self, text_a, text_b):
        self.text_a = text_a
        self.text_b = text_b

    def change_text(self):
        if self.isChecked():
            self.setText(self.text_b)
        else:
            self.setText(self.text_a)