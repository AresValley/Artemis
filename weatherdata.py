import re
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from threads import (BaseDownloadThread,
                     UpdateSpaceWeatherThread,
                     ThreadStatus,
                     UpdateForecastThread)
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


class ForecastData(_BaseWeatherData):
    """3-day forecast class. Extends _BaseWeatherData."""

    ROW_KEYWORDS = {
        "solar_row": "S1 or greater",
        "event_row": "III.  Event probabilities",
        "rb_now_row": "R1-R2",
        "ga_now_row": "Geomagnetic Activity Probabilities",
        "kp_index_row": "NOAA Kp index breakdown"
    }

    def __init__(self, parent):
        """Initialize all attributes and connect the thread to _parse_and_emit_signal."""
        super().__init__()
        self.forecast = ''
        self.probabilities = ''
        self.__labels_table = []
        self.__solar_row = None
        self.__event_row = None
        self.__rb_now_row = None
        self.__ga_now_row = None
        self.__kp_index_row = None
        self._update_thread = UpdateForecastThread(self)
        self._update_thread.finished.connect(self._parse_and_emit_signal)
        # Cannot use '__' here because of the for loop below.
        self._today_lbl = parent.today_lbl
        self._today_p1_lbl = parent.today_p1_lbl
        self._today_p2_lbl = parent.today_p2_lbl
        self.__today_lbls = []
        self.__today_p1_lbls = []
        self.__today_p2_lbls = []
        self.__all_lbls = []
        flags = ['', 'p1_', 'p2_']
        for flag in flags:
            title_lbl = getattr(self, "_today_" + flag + "lbl")
            title_lbl.setText("-")
            for index in range(20):
                label = getattr(
                    parent,
                    "forecast_today_" + flag + str(index) + "_lbl"
                )
                label.setText(Constants.UNKNOWN)
                if flag == flags[0]:
                    self.__today_lbls.append(label)
                if flag == flags[1]:
                    self.__today_p1_lbls.append(label)
                if flag == flags[2]:
                    self.__today_p2_lbls.append(label)

        self.__all_lbls = [
            self.__today_lbls,
            self.__today_p1_lbls,
            self.__today_p2_lbls
        ]

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

    def __split_lists(self):
        """Split the elements of forecast and probabilities."""
        self.forecast = [i.split() for i in self.forecast]
        self.probabilities = [i.split() for i in self.probabilities]

    def __find_row_with(self, data, text):
        """Given a list of strings, return the index of the first string containing the target text."""
        for i, row in enumerate(data):
            if text in row:
                return i
        return None

    def __get_rows(self):
        """Set all the rows needed for updating the screen.

        Raise an exception if something goes wrong."""
        self.__solar_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["solar_row"]
        )
        self.__event_row = self.__find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["event_row"]
        )
        self.__rb_now_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["rb_now_row"]
        )
        self.__ga_now_row = self.__find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["ga_now_row"]
        )
        self.__kp_index_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["kp_index_row"]
        )

        if any([
            self.__solar_row is None,
            self.__event_row is None,
            self.__rb_now_row is None,
            self.__ga_now_row is None,
            self.__kp_index_row is None
        ]):
            raise Exception('Missing Rows')

    def __set_dates(self):
        """Set the date labels."""
        month = self.forecast[self.__solar_row - 1][0]
        today = self.forecast[self.__solar_row - 1][1]
        today_p1 = self.forecast[self.__solar_row - 1][3]
        today_p2 = self.forecast[self.__solar_row - 1][5]
        self._today_lbl.setText(month + ' ' + today)
        self._today_p1_lbl.setText(month + ' ' + today_p1)
        self._today_p2_lbl.setText(month + ' ' + today_p2)

    def __make_labels_table(self):
        """Organize all the arguments to feed __get_lbl_value."""
        get_first_split = lambda x: x.split("/")[0]
        get_second_split = lambda x: x.split("/")[1]
        get_third_split = lambda x: x.split("/")[2]
        self.__labels_table = [
            [
                [self.forecast, self.__solar_row, 3, None],
                [self.probabilities, self.__event_row + 1, 2, get_first_split],
                [self.probabilities, self.__event_row + 2, 2, get_first_split],
                [self.probabilities, self.__event_row + 3, 1, get_first_split],
                [self.forecast, self.__rb_now_row, 1, None],
                [self.forecast, self.__rb_now_row + 1, 3, None],
                [self.probabilities, self.__ga_now_row + 2, 1, get_first_split],
                [self.probabilities, self.__ga_now_row + 3, 2, get_first_split],
                [self.probabilities, self.__ga_now_row + 4, 2, get_first_split],
                [self.probabilities, self.__ga_now_row + 6, 1, get_first_split],
                [self.probabilities, self.__ga_now_row + 7, 2, get_first_split],
                [self.probabilities, self.__ga_now_row + 8, 2, get_first_split],
                [self.forecast, self.__kp_index_row + 3, 1, None],
                [self.forecast, self.__kp_index_row + 4, 1, None],
                [self.forecast, self.__kp_index_row + 5, 1, None],
                [self.forecast, self.__kp_index_row + 6, 1, None],
                [self.forecast, self.__kp_index_row + 7, 1, None],
                [self.forecast, self.__kp_index_row + 8, 1, None],
                [self.forecast, self.__kp_index_row + 9, 1, None],
                [self.forecast, self.__kp_index_row + 10, 1, None]
            ],
            [
                [self.forecast, self.__solar_row, 4, None],
                [self.probabilities, self.__event_row + 1, 2, get_second_split],
                [self.probabilities, self.__event_row + 2, 2, get_second_split],
                [self.probabilities, self.__event_row + 3, 1, get_second_split],
                [self.forecast, self.__rb_now_row, 2, None],
                [self.forecast, self.__rb_now_row + 1, 4, None],
                [self.probabilities, self.__ga_now_row + 2, 1, get_second_split],
                [self.probabilities, self.__ga_now_row + 3, 2, get_second_split],
                [self.probabilities, self.__ga_now_row + 4, 2, get_second_split],
                [self.probabilities, self.__ga_now_row + 6, 1, get_second_split],
                [self.probabilities, self.__ga_now_row + 7, 2, get_second_split],
                [self.probabilities, self.__ga_now_row + 8, 2, get_second_split],
                [self.forecast, self.__kp_index_row + 3, 2, None],
                [self.forecast, self.__kp_index_row + 4, 2, None],
                [self.forecast, self.__kp_index_row + 5, 2, None],
                [self.forecast, self.__kp_index_row + 6, 2, None],
                [self.forecast, self.__kp_index_row + 7, 2, None],
                [self.forecast, self.__kp_index_row + 8, 2, None],
                [self.forecast, self.__kp_index_row + 9, 2, None],
                [self.forecast, self.__kp_index_row + 10, 2, None]
            ],
            [
                [self.forecast, self.__solar_row, 5, None],
                [self.probabilities, self.__event_row + 1, 2, get_third_split],
                [self.probabilities, self.__event_row + 2, 2, get_third_split],
                [self.probabilities, self.__event_row + 3, 1, get_third_split],
                [self.forecast, self.__rb_now_row, 3, None],
                [self.forecast, self.__rb_now_row + 1, 5, None],
                [self.probabilities, self.__ga_now_row + 2, 1, get_third_split],
                [self.probabilities, self.__ga_now_row + 3, 2, get_third_split],
                [self.probabilities, self.__ga_now_row + 4, 2, get_third_split],
                [self.probabilities, self.__ga_now_row + 6, 1, get_third_split],
                [self.probabilities, self.__ga_now_row + 7, 2, get_third_split],
                [self.probabilities, self.__ga_now_row + 8, 2, get_third_split],
                [self.forecast, self.__kp_index_row + 3, 3, None],
                [self.forecast, self.__kp_index_row + 4, 3, None],
                [self.forecast, self.__kp_index_row + 5, 3, None],
                [self.forecast, self.__kp_index_row + 6, 3, None],
                [self.forecast, self.__kp_index_row + 7, 3, None],
                [self.forecast, self.__kp_index_row + 8, 3, None],
                [self.forecast, self.__kp_index_row + 9, 3, None],
                [self.forecast, self.__kp_index_row + 10, 3, None]
            ]
        ]

    def __get_lbl_value(self, data, row, col, f=None):
        """Return the well-formatted string-value of the label."""
        val = data[row][col]
        if f is not None:
            val = f(val)
        val = val.rstrip('%')
        if len(val) > 1:
            val = val.lstrip('0')
        return val

    def __set_labels_values(self):
        """Set all the labels values."""
        for lbl_list, table in zip(self.__all_lbls, self.__labels_table):
            for lbl, row in zip(lbl_list, table):
                lbl.switch_off()
                value = self.__get_lbl_value(*row)
                lbl.level = safe_cast(value, int)
                if not isinstance(lbl, MultiColorSwitchableLabel):
                    value += '%'
                lbl.setText(value)
                lbl.switch_on()

    def update_all_labels(self):
        """Update all the labels values.

        If an exception is raised in the process, do nothing."""
        try:
            self.__get_rows()
            self.__split_lists()
            self.__make_labels_table()
            self.__set_dates()
            self.__set_labels_values()
        except Exception:
            pass

    def remove_data(self):
        """Remove the reference to the downloaded data."""
        self.forecast = ''
        self.probabilities = ''
