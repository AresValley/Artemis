import re
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from threads import (BaseDownloadThread,
                     UpdateSpaceWeatherThread,
                     ThreadStatus,
                     UpdateForecastThread)
from constants import Constants
from switchable_label import MultiColorSwitchableLabel


class _BaseWeatherData(QObject):
    update_complete = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._update_thread = BaseDownloadThread()

    @property
    def is_updating(self):
        return self._update_thread.isRunning()

    def update(self):
        self._update_thread.start()

    def _parse_data(self):
        pass

    @pyqtSlot()
    def _parse_and_emit_signal(self):
        status_ok = False
        if self._update_thread.status is ThreadStatus.OK:
            status_ok = True
            self._parse_data()
        self.update_complete.emit(status_ok)

    def _double_split(self, string):
        return [i.split() for i in string.splitlines()]

    def shutdown_thread(self):
        self._update_thread.terminate()
        self._update_thread.wait()


class SpaceWeatherData(_BaseWeatherData):
    def __init__(self):
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
        self.xray      = self._double_split(self.xray)
        self.prot_el   = self._double_split(self.prot_el)
        self.ak_index  = self._double_split(self.ak_index)
        self.sgas      = self._double_split(self.sgas)
        self.geo_storm = self._double_split(self.geo_storm)

    def remove_data(self):
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

    ROW_KEYWORDS = {
        "solar_row": "S1 or greater",
        "event_row": "III.  Event probabilities",
        "rb_now_row": "R1-R2",
        "ga_now_row": "Geomagnetic Activity Probabilities",
        "kp_index_row": "NOAA Kp index breakdown"
    }

    def __init__(self, parent):
        super().__init__()
        self.forecast = ''
        self.probabilities = ''
        self.labels_table = []
        self.solar_row = None
        self.event_row = None
        self.rb_now_row = None
        self.ga_now_row = None
        self.kp_index_row = None
        self._update_thread = UpdateForecastThread(self)
        self._update_thread.finished.connect(self._parse_and_emit_signal)
        self.today_lbl = parent.today_lbl
        self.today_p1_lbl = parent.today_p1_lbl
        self.today_p2_lbl = parent.today_p2_lbl
        self.__today_lbls = []
        self.__today_p1_lbls = []
        self.__today_p2_lbls = []
        self.__all_lbls = []
        flags = ['', 'p1_', 'p2_']
        for flag in flags:
            title_lbl = getattr(self, "today_" + flag + "lbl")
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
        self.forecast = self.forecast.splitlines()
        # Remove possible '(G\d)' from the kp_index table
        self.probabilities = re.sub('(G\d)', lambda obj: '', self.probabilities)
        self.probabilities = self.probabilities.splitlines()

    def __split_lists(self):
        self.forecast = [i.split() for i in self.forecast]
        self.probabilities = [i.split() for i in self.probabilities]

    def __find_row_with(self, data, text):
        for i, row in enumerate(data):
            if text in row:
                return i
        return None

    def __get_rows(self):
        self.solar_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["solar_row"]
        )
        self.event_row = self.__find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["event_row"]
        )
        self.rb_now_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["rb_now_row"]
        )
        self.ga_now_row = self.__find_row_with(
            self.probabilities,
            self.ROW_KEYWORDS["ga_now_row"]
        )
        self.kp_index_row = self.__find_row_with(
            self.forecast,
            self.ROW_KEYWORDS["kp_index_row"]
        )

        is_none = lambda x: x is None
        if any([
            is_none(self.solar_row),
            is_none(self.event_row),
            is_none(self.rb_now_row),
            is_none(self.ga_now_row),
            is_none(self.kp_index_row)
        ]):
            raise Exception

    def __set_dates(self):
        month = self.forecast[self.solar_row - 1][0]
        today = self.forecast[self.solar_row - 1][1]
        today_p1 = self.forecast[self.solar_row - 1][3]
        today_p2 = self.forecast[self.solar_row - 1][5]
        self.today_lbl.setText(month + ' ' + today)
        self.today_p1_lbl.setText(month + ' ' + today_p1)
        self.today_p2_lbl.setText(month + ' ' + today_p2)

    def __make_labels_table(self):
        get_first_split = lambda x: x.split("/")[0]
        get_second_split = lambda x: x.split("/")[1]
        get_third_split = lambda x: x.split("/")[2]
        self.labels_table = [
            [
                [self.forecast, self.solar_row, 3, None],
                [self.probabilities, self.event_row + 1, 2, get_first_split],
                [self.probabilities, self.event_row + 2, 2, get_first_split],
                [self.probabilities, self.event_row + 3, 1, get_first_split],
                [self.forecast, self.rb_now_row, 1, None],
                [self.forecast, self.rb_now_row + 1, 3, None],
                [self.probabilities, self.ga_now_row + 2, 1, get_first_split],
                [self.probabilities, self.ga_now_row + 3, 2, get_first_split],
                [self.probabilities, self.ga_now_row + 4, 2, get_first_split],
                [self.probabilities, self.ga_now_row + 6, 1, get_first_split],
                [self.probabilities, self.ga_now_row + 7, 2, get_first_split],
                [self.probabilities, self.ga_now_row + 8, 2, get_first_split],
                [self.forecast, self.kp_index_row + 3, 1, None],
                [self.forecast, self.kp_index_row + 4, 1, None],
                [self.forecast, self.kp_index_row + 5, 1, None],
                [self.forecast, self.kp_index_row + 6, 1, None],
                [self.forecast, self.kp_index_row + 7, 1, None],
                [self.forecast, self.kp_index_row + 8, 1, None],
                [self.forecast, self.kp_index_row + 9, 1, None],
                [self.forecast, self.kp_index_row + 10, 1, None]
            ],
            [
                [self.forecast, self.solar_row, 4, None],
                [self.probabilities, self.event_row + 1, 2, get_second_split],
                [self.probabilities, self.event_row + 2, 2, get_second_split],
                [self.probabilities, self.event_row + 3, 1, get_second_split],
                [self.forecast, self.rb_now_row, 2, None],
                [self.forecast, self.rb_now_row + 1, 4, None],
                [self.probabilities, self.ga_now_row + 2, 1, get_second_split],
                [self.probabilities, self.ga_now_row + 3, 2, get_second_split],
                [self.probabilities, self.ga_now_row + 4, 2, get_second_split],
                [self.probabilities, self.ga_now_row + 6, 1, get_second_split],
                [self.probabilities, self.ga_now_row + 7, 2, get_second_split],
                [self.probabilities, self.ga_now_row + 8, 2, get_second_split],
                [self.forecast, self.kp_index_row + 3, 2, None],
                [self.forecast, self.kp_index_row + 4, 2, None],
                [self.forecast, self.kp_index_row + 5, 2, None],
                [self.forecast, self.kp_index_row + 6, 2, None],
                [self.forecast, self.kp_index_row + 7, 2, None],
                [self.forecast, self.kp_index_row + 8, 2, None],
                [self.forecast, self.kp_index_row + 9, 2, None],
                [self.forecast, self.kp_index_row + 10, 2, None]
            ],
            [
                [self.forecast, self.solar_row, 5, None],
                [self.probabilities, self.event_row + 1, 2, get_third_split],
                [self.probabilities, self.event_row + 2, 2, get_third_split],
                [self.probabilities, self.event_row + 3, 1, get_third_split],
                [self.forecast, self.rb_now_row, 3, None],
                [self.forecast, self.rb_now_row + 1, 5, None],
                [self.probabilities, self.ga_now_row + 2, 1, get_third_split],
                [self.probabilities, self.ga_now_row + 3, 2, get_third_split],
                [self.probabilities, self.ga_now_row + 4, 2, get_third_split],
                [self.probabilities, self.ga_now_row + 6, 1, get_third_split],
                [self.probabilities, self.ga_now_row + 7, 2, get_third_split],
                [self.probabilities, self.ga_now_row + 8, 2, get_third_split],
                [self.forecast, self.kp_index_row + 3, 3, None],
                [self.forecast, self.kp_index_row + 4, 3, None],
                [self.forecast, self.kp_index_row + 5, 3, None],
                [self.forecast, self.kp_index_row + 6, 3, None],
                [self.forecast, self.kp_index_row + 7, 3, None],
                [self.forecast, self.kp_index_row + 8, 3, None],
                [self.forecast, self.kp_index_row + 9, 3, None],
                [self.forecast, self.kp_index_row + 10, 3, None]
            ]
        ]

    def __get_lbl_value(self, data, row, col, f = None):
        val = data[row][col]
        if f is not None:
            val = f(val)
        val = val.lstrip('0').rstrip('%')
        return val

    def __is_integer(self, s):
        try:
            int(s)
        except Exception:
            return False
        else:
            return True

    def __set_labels_values(self):
        for lbl_list, table in zip(self.__all_lbls, self.labels_table):
            for lbl, row in zip(lbl_list, table):
                lbl.switch_off()
                value = self.__get_lbl_value(*row)
                if self.__is_integer(value):
                    lbl.level = int(value)
                if not isinstance(lbl, MultiColorSwitchableLabel):
                    value += '%'
                lbl.setText(value)
                lbl.switch_on()

    def update_all_labels(self):
        try:
            self.__get_rows()
            self.__split_lists()
            self.__make_labels_table()
            self.__set_dates()
            self.__set_labels_values()
        except Exception:
            pass

    def remove_data(self):
        self.forecast = ''
        self.probabilities = ''
