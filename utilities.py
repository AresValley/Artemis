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
    db_location = _ReadOnlyProperty('https://aresvalley.com/Storage/Artemis/Database/data.zip')
    ref_loc = _ReadOnlyProperty('https://aresvalley.com/Storage/Artemis/Database/data.zip.log')
    data_folder = _ReadOnlyProperty('Data')
    spectra_folder = _ReadOnlyProperty('Spectra')
    audio_folder = _ReadOnlyProperty('Audio')
    icons_folder = _ReadOnlyProperty('icons_imgs')
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
    bands = _ReadOnlyProperty((__ELF, __SLF, __ULF, __VLF, __LF, __MF, __HF, __VHF, __UHF, __SHF, __EHF))
    active_color = _ReadOnlyProperty("#39eaff")
    inactive_color = _ReadOnlyProperty("#9f9f9f")
    conversion_factors = _ReadOnlyProperty({"Hz":1, "kHz":1000, "MHz":1000000, "GHz":1000000000})
    modes = _ReadOnlyProperty({"FM": ["NFM", "WFM"],
                               "AM": [],
                               "CW": [],
                               "SK": ["FSK", "PSK", "MSK"],
                               "SB": ["LSB", "USB", "DSB"],
                               "Chirp Spread Spectrum": [],
                               "FHSS-TDM": [],
                               "RAW": [],
                               "SC-FDMA": [],}
                             )
    unknown = "Unknown"


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
        reference = read_csv(Constants.ref_loc, delimiter = '*').iat[-1, n]
    except HTTPError:
        return False
    return code.hexdigest() == reference