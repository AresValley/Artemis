from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal


class UIAudioAnalysis(QObject):
    # Python > QML Signals
    show_ui = Signal()

    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/AudioAnalysis.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()

    def _connect(self):
        # QML > Python connections

        # Python > QML connections
        self.show_ui.connect(self._window.show)

    def load_audioanalysis_ui(self):
        self.show_ui.emit()


