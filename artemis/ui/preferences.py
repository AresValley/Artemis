from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

from artemis.utils.config_utils import *


class UIPreferences(QObject):
    # Python > QML Signals
    show_ui = Signal()
    load_material_accent = Signal(str)
    load_material_theme = Signal(str)
    load_autoload = Signal(int)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/Preferences.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.saveMaterialAccent.connect(self.save_material_accent)
        self._window.saveMaterialTheme.connect(self.save_material_theme)
        self._window.saveAutoload.connect(self.save_autoload)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.load_material_accent.connect(self._window.loadMaterialAccent)
        self.load_material_theme.connect(self._window.loadMaterialTheme)
        self.load_autoload.connect(self._window.loadAutoload)


    def load_preferences_ui(self):
        """ Loading all the initial preferences from the conf file to the UI
        """
        self.load_material_accent.emit(CONFIGURE_QT.value("Material", "Accent", "Green"))
        self.load_material_theme.emit(CONFIGURE_QT.value("Material", "Theme", "System"))
        self.load_autoload.emit(int(CONFIGURE_QT.value("Database", "autoload", 0)))
        self.show_ui.emit()


    @Slot(str)
    def save_material_accent(self, material_accent):
        """ Saving material accent setting
        """
        CONFIGURE_QT.set("Material", "Accent", material_accent)


    @Slot(str)
    def save_material_theme(self, material_theme):
        """ Saving material theme setting
        """
        CONFIGURE_QT.set("Material", "Theme", material_theme)


    @Slot(int)
    def save_autoload(self, autoload):
        """ Saving autoload setting
        """
        CONFIGURE_QT.set("Database", "autoload", str(autoload))
