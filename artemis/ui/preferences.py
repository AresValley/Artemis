from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

from artemis.utils.config_utils import CONFIGURE_QT


class UIPreferences(QObject):
    # Python > QML Signals
    show_ui = Signal()
    load_material_accent = Signal(str)
    load_material_theme = Signal(str)
    load_language = Signal(str)
    load_scaling = Signal(str)
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
        self._window.saveLocalizationLanguage.connect(self.save_language)
        self._window.saveScaling.connect(self.save_scaling)
        self._window.saveAutoload.connect(self.save_autoload)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.load_material_accent.connect(self._window.loadMaterialAccent)
        self.load_material_theme.connect(self._window.loadMaterialTheme)
        self.load_language.connect(self._window.loadLocalizationLanguage)
        self.load_scaling.connect(self._window.loadScaling)
        self.load_autoload.connect(self._window.loadAutoload)


    def load_preferences_ui(self):
        """ Loading all the initial preferences from the conf file to the UI
        """
        self.load_material_accent.emit(CONFIGURE_QT.value("Material", "Accent", "Green"))
        self.load_material_theme.emit(CONFIGURE_QT.value("Material", "Theme", "System"))
        self.load_language.emit(CONFIGURE_QT.value('Localization', 'language', 'en_US'))
        self.load_scaling.emit(CONFIGURE_QT.value("Scaling", "factor", "1.00"))
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


    @Slot(str)
    def save_language(self, language):
        """ Saving language
        """
        CONFIGURE_QT.set("Localization", "language", language)


    @Slot(str)
    def save_scaling(self, scaling):
        """ Saving UI scaling
        """
        CONFIGURE_QT.set("Scaling", "factor", scaling)


    @Slot(int)
    def save_autoload(self, autoload):
        """ Saving autoload setting
        """
        CONFIGURE_QT.set("Database", "autoload", str(autoload))
