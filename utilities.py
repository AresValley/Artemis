from collections import namedtuple
import hashlib
from pandas import read_csv

class _ReadOnlyProperty(object):
    def __init__(self, value):
        self.value = value
    
    def __get__(self, obj, objtype):
        return self.value

    def __Set__(self, obj, value):
        return NotImplementedError("Cannot change a constant.")


class Constants(object):
    DB_LOCATION = _ReadOnlyProperty('https://aresvalley.com/Storage/Artemis/Database/data.zip')
    REF_LOC = _ReadOnlyProperty('https://aresvalley.com/Storage/Artemis/Database/data.zip.log')
    DATA_FOLDER = _ReadOnlyProperty('Data')
    SPECTRA_FOLDER = _ReadOnlyProperty('Spectra')
    AUDIO_FOLDER = _ReadOnlyProperty('Audio')
    ICONS_FOLDER = _ReadOnlyProperty('icons_imgs')
    __Band = namedtuple("Band", ["lower", "upper"])
    __ELF = __Band(0, 30) # Formally it is (3, 30) Hz.
    __SLF = __Band(30, 300)
    __ULF = __Band(300, 3000)
    __VLF = __Band(3000, 30000)
    __LF  = __Band(30 * 10**3, 300 * 10**3)
    __MF  = __Band(300 * 10 ** 3, 3000 * 10**3)
    __HF  = __Band(3 * 10**6, 30 * 10**6)
    __VHF = __Band(30 * 10**6, 300 * 10**6)
    __UHF = __Band(300 * 10**6, 3000 * 10**6)
    __SHF = __Band(3 * 10**9, 30 * 10**9)
    __EHF = __Band(30 * 10**9, 300 * 10**9)
    BANDS = _ReadOnlyProperty((__ELF, __SLF, __ULF, __VLF, __LF, __MF, __HF, __VHF, __UHF, __SHF, __EHF))
    ACTIVE_COLOR = _ReadOnlyProperty("#39eaff")
    INACTIVE_COLOR = _ReadOnlyProperty("#9f9f9f")
    CONVERSION_FACTORS = _ReadOnlyProperty({"Hz":1, "kHz":1000, "MHz":1000000, "GHz":1000000000})
    MODES = _ReadOnlyProperty({"FM": ["NFM", "WFM"],
                               "AM": [],
                               "CW": [],
                               "SK": ["FSK", "PSK", "MSK"],
                               "SB": ["LSB", "USB", "DSB"],
                               "Chirp Spread Spectrum": [],
                               "FHSS-TDM": [],
                               "RAW": [],
                               "SC-FDMA": [],}
                             )
    UNKNOWN = "Unknown"


def reset_apply_remove_btn(button):
    if button.isChecked():
        button.setChecked(False)
        button.clicked.emit()


def checksum_ok(data, what):
    code = hashlib.sha256()
    code.update(data)
    if what == "folder":
        n = 0
    elif what == "db":
        n = 1
    else:
        raise ValueError("Wrong entry name.")
    try:
        reference = read_csv(Constants.REF_LOC, delimiter = '*').iat[-1, n]
    except HTTPError:
        return False
    return code.hexdigest() == reference