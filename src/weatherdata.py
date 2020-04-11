import logging
import re
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from threads import (
    BaseDownloadThread,
    UpdateSpaceWeatherThread,
    ThreadStatus,
    UpdateForecastThread
)
from constants import Constants
from switchable_label import MultiColorSwitchableLabel
from utilities import safe_cast


class _BaseWeatherData(QObject):
    """Base class for the weather data. Extends QObject."""

    update_complete = pyqtSignal(bool)

    def __init__(self):
        """Create a BaseDownloadThread object."""
        super().__init__()
        self._update_thread = BaseDownloadThread()

    @property
    def is_updating(self):
        """Return whether the thread is running."""
        return self._update_thread.isRunning()

    def update(self):
        """Start the thread."""
        self._update_thread.start()

    def _parse_data(self):
        """Dummy function. Must be overrided by subclasses."""
        pass

    @pyqtSlot()
    def _parse_and_emit_signal(self):
        """Parse the data and emit an 'update_complete' signal.

        If the download was not successful, do not parse the data.
        The 'update_complete' signal propagates the thread status up to the
        calling slot."""
        status_ok = False
        if self._update_thread.status is ThreadStatus.OK:
            status_ok = True
            self._parse_data()
        self.update_complete.emit(status_ok)

    def _double_split(self, string):
        """Given a string, return a list of lists.

        First split on each line. Then split each line on whitespaces."""
        return [i.split() for i in string.splitlines()]

    def shutdown_thread(self):
        """Terminate the download thread."""
        self._update_thread.terminate()
        self._update_thread.wait()


class SpaceWeatherData(_BaseWeatherData):
    """Space weather class. Extends _BaseWeatherData."""

    def __init__(self):
        """Set all attributes and connect the thread to _parse_and_emit_signal."""
        super().__init__()
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''
        self.images = [
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap()
        ]
        self._update_thread = UpdateSpaceWeatherThread(self)
        self._update_thread.finished.connect(self._parse_and_emit_signal)

    def _parse_data(self):
        """Override _BaseWeatherData._parse_data.

        Set all the data."""
        self.xray      = self._double_split(self.xray)
        self.prot_el   = self._double_split(self.prot_el)
        self.ak_index  = self._double_split(self.ak_index)
        self.sgas      = self._double_split(self.sgas)
        self.geo_storm = self._double_split(self.geo_storm)

    def remove_data(self):
        """Remove the reference to all the data."""
        self.xray = ''
        self.prot_el = ''
        self.ak_index = ''
        self.sgas = ''
        self.geo_storm = ''
        self.images = [
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap(),
            QPixmap()
        ]


def _make_labels_table(forecast, probabilities, rows):
    """Organize all the arguments to feed _get_lbl_value."""
    def get_first_split(x):
        return x.split("/")[0]

    def get_second_split(x):
        return x.split("/")[1]

    def get_third_split(x):
        return x.split("/")[2]

    solar_row = rows["solar_row"]
    event_row = rows["event_row"]
    rb_now_row = rows["rb_now_row"]
    ga_now_row = rows["ga_now_row"]
    kp_index_row = rows["kp_index_row"]
    return [
        [
            [forecast, solar_row, 3, None],
            [probabilities, event_row + 1, 2, get_first_split],
            [probabilities, event_row + 2, 2, get_first_split],
            [probabilities, event_row + 3, 1, get_first_split],
            [forecast, rb_now_row, 1, None],
            [forecast, rb_now_row + 1, 3, None],
            [probabilities, ga_now_row + 2, 1, get_first_split],
            [probabilities, ga_now_row + 3, 2, get_first_split],
            [probabilities, ga_now_row + 4, 2, get_first_split],
            [probabilities, ga_now_row + 6, 1, get_first_split],
            [probabilities, ga_now_row + 7, 2, get_first_split],
            [probabilities, ga_now_row + 8, 2, get_first_split],
            [forecast, kp_index_row + 3, 1, None],
            [forecast, kp_index_row + 4, 1, None],
            [forecast, kp_index_row + 5, 1, None],
            [forecast, kp_index_row + 6, 1, None],
            [forecast, kp_index_row + 7, 1, None],
            [forecast, kp_index_row + 8, 1, None],
            [forecast, kp_index_row + 9, 1, None],
            [forecast, kp_index_row + 10, 1, None]
        ],
        [
            [forecast, solar_row, 4, None],
            [probabilities, event_row + 1, 2, get_second_split],
            [probabilities, event_row + 2, 2, get_second_split],
            [probabilities, event_row + 3, 1, get_second_split],
            [forecast, rb_now_row, 2, None],
            [forecast, rb_now_row + 1, 4, None],
            [probabilities, ga_now_row + 2, 1, get_second_split],
            [probabilities, ga_now_row + 3, 2, get_second_split],
            [probabilities, ga_now_row + 4, 2, get_second_split],
            [probabilities, ga_now_row + 6, 1, get_second_split],
            [probabilities, ga_now_row + 7, 2, get_second_split],
            [probabilities, ga_now_row + 8, 2, get_second_split],
            [forecast, kp_index_row + 3, 2, None],
            [forecast, kp_index_row + 4, 2, None],
            [forecast, kp_index_row + 5, 2, None],
            [forecast, kp_index_row + 6, 2, None],
            [forecast, kp_index_row + 7, 2, None],
            [forecast, kp_index_row + 8, 2, None],
            [forecast, kp_index_row + 9, 2, None],
            [forecast, kp_index_row + 10, 2, None]
        ],
        [
            [forecast, solar_row, 5, None],
            [probabilities, event_row + 1, 2, get_third_split],
            [probabilities, event_row + 2, 2, get_third_split],
            [probabilities, event_row + 3, 1, get_third_split],
            [forecast, rb_now_row, 3, None],
            [forecast, rb_now_row + 1, 5, None],
            [probabilities, ga_now_row + 2, 1, get_third_split],
            [probabilities, ga_now_row + 3, 2, get_third_split],
            [probabilities, ga_now_row + 4, 2, get_third_split],
            [probabilities, ga_now_row + 6, 1, get_third_split],
            [probabilities, ga_now_row + 7, 2, get_third_split],
            [probabilities, ga_now_row + 8, 2, get_third_split],
            [forecast, kp_index_row + 3, 3, None],
            [forecast, kp_index_row + 4, 3, None],
            [forecast, kp_index_row + 5, 3, None],
            [forecast, kp_index_row + 6, 3, None],
            [forecast, kp_index_row + 7, 3, None],
            [forecast, kp_index_row + 8, 3, None],
            [forecast, kp_index_row + 9, 3, None],
            [forecast, kp_index_row + 10, 3, None]
        ]
    ]


def _get_lbl_value(data, row, col, f=None):
    """Return the well-formatted string-value of the label."""
    val = data[row][col]
    if f is not None:
        val = f(val)
    val = val.rstrip('%')
    if len(val) > 1:
        val = val.lstrip('0')
    return val


class ForecastData(_BaseWeatherData):
    """3-day forecast class. Extends _BaseWeatherData."""

    ROW_KEYWORDS = {
        "solar_row": "S1 or greater",
        "event_row": "III.  Event probabilities",
        "rb_now_row": "R1-R2",
        "ga_now_row": "Geomagnetic Activity Probabilities",
        "kp_index_row": "NOAA Kp index breakdown"
    }

    LABELS_PER_COLUMN = 20

    def __init__(self, owner):
        """Initialize all attributes and connect the thread to _parse_and_emit_signal."""
        super().__init__()
        self.forecast = []
        self.probabilities = []
        self._update_thread = UpdateForecastThread(self)
        self._update_thread.finished.connect(self._parse_and_emit_signal)
        self._today_lbl = owner.today_lbl
        self._today_p1_lbl = owner.today_p1_lbl
        self._today_p2_lbl = owner.today_p2_lbl
        today_lbls = []
        today_p1_lbls = []
        today_p2_lbls = []
        flags = ['', 'p1_', 'p2_']
        for flag in flags:
            title_lbl = getattr(self, "_today_" + flag + "lbl")
            title_lbl.setText("-")
            for index in range(self.LABELS_PER_COLUMN):
                label = getattr(
                    owner,
                    "forecast_today_" + flag + str(index) + "_lbl"
                )
                label.setText(Constants.UNKNOWN)
                if flag == flags[0]:
                    today_lbls.append(label)
                if flag == flags[1]:
                    today_p1_lbls.append(label)
                if flag == flags[2]:
                    today_p2_lbls.append(label)

        self._all_lbls = [today_lbls, today_p1_lbls, today_p2_lbls]

    def _parse_data(self):
        """Override _BaseWeatherData._parse_data.

        Set all the relevant data."""
        # Remove possible '(G\d)' from the kp_index table
        self.forecast = re.sub(
            '\(G\d\)', lambda obj: '', self.forecast
        )
        self.forecast = self.forecast.splitlines()
        self.probabilities = re.sub(
            '\(G\d\)', lambda obj: '', self.probabilities
        )
        self.probabilities = self.probabilities.splitlines()

    def _split_lists(self):
        """Split the elements of forecast and probabilities."""
        return [i.split() for i in self.forecast], [i.split() for i in self.probabilities]

    def _find_row_with(self, data, text):
        """Given a list of strings, return the index of the first string containing the target text."""
        for i, row in enumerate(data):
            if text in row:
                return i
        return None

    def _get_rows(self):
        """Get all the rows needed for updating the screen.

        Raise an exception if something goes wrong."""

        rows = {}
        rows["solar_row"] = self._find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["solar_row"]
        )
        rows["event_row"] = self._find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["event_row"]
        )
        rows["rb_now_row"] = self._find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["rb_now_row"]
        )
        rows["ga_now_row"] = self._find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["ga_now_row"]
        )
        rows["kp_index_row"] = self._find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["kp_index_row"]
        )

        if any(row is None for row in rows.values()):
            raise Exception('Missing Rows')
        else:
            return rows

    def _set_dates(self, forecast, solar_row):
        """Set the date labels."""
        month = forecast[solar_row - 1][0]
        today = forecast[solar_row - 1][1]
        today_p1 = forecast[solar_row - 1][3]
        today_p2 = forecast[solar_row - 1][5]
        self._today_lbl.setText(month + ' ' + today)
        self._today_p1_lbl.setText(month + ' ' + today_p1)
        self._today_p2_lbl.setText(month + ' ' + today_p2)

    def _set_labels_values(self, labels_table):
        """Set all the labels values."""
        for lbl_list, table in zip(self._all_lbls, labels_table):
            for lbl, row in zip(lbl_list, table):
                lbl.switch_off()
                value = _get_lbl_value(*row)
                lbl.level = safe_cast(value, int)
                if not isinstance(lbl, MultiColorSwitchableLabel):
                    value += '%'
                lbl.setText(value)
                lbl.switch_on()

    def update_all_labels(self):
        """Update all the labels values.

        If an exception is raised in the process, do nothing."""
        try:
            rows = self._get_rows()
            forecast, probabilities = self._split_lists()
            labels_table = _make_labels_table(forecast, probabilities, rows)
            self._set_dates(forecast, rows["solar_row"])
            self._set_labels_values(labels_table)
        except Exception:
            logging.error("Update ForecastData failure")
            pass

    def remove_data(self):
        """Remove the reference to the downloaded data."""
        self.forecast = []
        self.probabilities = []
