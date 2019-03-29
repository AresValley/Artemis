from functools import partial
import hashlib
import re
import sys
import os
from pandas import read_csv

from PyQt5.QtWidgets import QMessageBox

import constants

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def uncheck_and_emit(button):
    if button.isChecked():
        button.setChecked(False)
        button.clicked.emit()

def pop_up(cls, title, text,
           informative_text = None,
           connection = None,
           is_question = False,
           default_btn = QMessageBox.Yes):
    msg = QMessageBox(cls)
    msg.setWindowTitle(title)
    msg.setText(text)
    if informative_text:
        msg.setInformativeText(informative_text)
    if connection:
        msg.finished.connect(connection)
    if is_question:
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(default_btn)
    msg.adjustSize()
    return msg

def checksum_ok(data, what):
    code = hashlib.sha256()
    code.update(data)
    if what == constants.ChecksumWhat.FOLDER:
        n = 0
    elif what == constants.ChecksumWhat.DB:
        n = 1
    else:
        raise ValueError("Wrong entry name.")
    try:
        reference = read_csv(constants.Database.LINK_REF,
                             delimiter = constants.Database.DELIMITER).iat[-1, n]
    except:
        raise
    return code.hexdigest() == reference

def is_valid_html_color(color):
    return bool(re.match("#([a-zA-Z0-9]){6}", color))

def connect_to(events_to_connect, fun_to_connect, fun_args):
    if fun_args:
        for event in events_to_connect:
            event.connect(partial(fun_to_connect, *fun_args))
    else:
        for event in events_to_connect:
            event.connect(fun_to_connect)

def filters_ok(spinbox, filter_unit, confidence, sign = 1):
        band_filter = spinbox.value() * constants.CONVERSION_FACTORS[filter_unit.currentText()]
        return band_filter + sign * (confidence.value() * band_filter) // 100

def is_undef_freq(current_signal):
    lower_freq = current_signal.at[constants.Signal.INF_FREQ]
    upper_freq = current_signal.at[constants.Signal.SUP_FREQ]
    return lower_freq == constants.UNKNOWN or upper_freq == constants.UNKNOWN

def is_undef_band(current_signal):
    lower_band = current_signal.at[constants.Signal.INF_BAND]
    upper_band = current_signal.at[constants.Signal.SUP_BAND]
    return lower_band == constants.UNKNOWN or upper_band == constants.UNKNOWN

def change_unit(num):
    digits = len(num)
    if digits < 4:
        return 1
    elif digits < 7:
        return 1000
    elif digits < 10:
        return 10**6
    else:
        return 10**9

def format_numbers(lower, upper):
    units = {1: 'Hz', 1000: 'kHz', 10**6: 'MHz', 10**9: 'GHz'}
    lower_factor = change_unit(lower)
    upper_factor = change_unit(upper)
    pre_lower = lower
    pre_upper = upper
    lower = int(lower) / lower_factor
    upper = int(upper) / upper_factor
    if lower.is_integer():
        lower = int(lower)
    if upper.is_integer():
        upper = int(upper)
    if pre_lower != pre_upper:
        return f"{lower:,} {units[lower_factor]} - {upper:,} {units[upper_factor]}"
    else:
        return f"{lower:,} {units[lower_factor]}"
