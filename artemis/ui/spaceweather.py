from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal

from artemis.utils.path_utils import *
from artemis.utils.generic_utils import *

from artemis.utils.constants import Constants


class UIspaceweather(QObject):
    # Python > QML Signals
    show_ui = Signal()
    load_poseidon_report = Signal(dict)
    load_poseidon_forecast_report = Signal(dict)
    load_poseidon_drap_report = Signal(dict)
    load_aurora_report = Signal()
    update_bottom_bar = Signal(str)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SpaceWeather.qml')
        self._window = self._engine.rootObjects()[0]

        self._window_current = self._window.findChild(QObject, "spaceWeatherCurrentObj")
        self._window_forecast = self._window.findChild(QObject, "spaceWeatherForecastObj")
        self._window_drap = self._window.findChild(QObject, "spaceWeatherDRAPObj")
        self._window_aurora = self._window.findChild(QObject, "spaceWeatherAuroraObj")

        self._connect()


    def _connect(self):
        # QML > Python connections

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.update_bottom_bar.connect(self._window.updateBottomBar)
        self.load_poseidon_report.connect(self._window_current.loadReport)
        self.load_poseidon_forecast_report.connect(self._window_forecast.loadForecastReport)
        self.load_poseidon_drap_report.connect(self._window_drap.loadDrapReport)
        self.load_aurora_report.connect(self._window_aurora.loadAuroraReport)


    def load_spaceweather_ui(self):
        """ Before opening the windows, poseidon report (data.json) is read online
        """
        self.download_poseidon_report()
    

    def download_poseidon_report(self):
        update_manager = self._parent.update_manager
        poseidon_data = update_manager.fetch_remote_json(
            Constants.POSEIDON_REPORT_URL,
            True
        )
        if poseidon_data:
            self.load_poseidon_report.emit(poseidon_data)
            self.load_poseidon_forecast_report.emit(poseidon_data)
            self.load_poseidon_drap_report.emit(poseidon_data)
            self.load_aurora_report.emit()

            self.update_bottom_bar.emit(
                'Loaded Poseidon report issued on {} at {} UTC'.format(
                    poseidon_data['JSON_INFO']['utc_date'],
                    poseidon_data['JSON_INFO']['utc_time']
                )
            )
            self.show_ui.emit()
