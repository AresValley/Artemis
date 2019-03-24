from collections import namedtuple
from enum import Enum, auto

class Ftype(object):
    FREQ = "freq"
    BAND = "band"

class GfdType(Enum):
    FREQ = auto()
    LOC  = auto()

class ChecksumWhat(Enum):
    FOLDER = auto()
    DB = auto()

class Messages(object):
    NO_DB_AVAIL       = "No database available.\nGo to Updates->Update database."
    NO_DB             = "No database"
    NO_CONNECTION     = "No internet connection"
    NO_CONNECTION_MSG = "Unable to establish an internet connection."
    BAD_DOWNLOAD      = "Something went wrong"
    BAD_DOWNLOAD_MSG  = "Something went wrong with the downaload.\nCheck your internet connection and try again."
    BAD_FILE          = "Bad file detected"
    BAD_FILE_MSG      = "The downloaded file seems to be corrupted.\nThe old database has not been deleted and\nthe downloaded file has been discarded."

class Signal(object):
    NAME          = "name"
    INF_FREQ      = "inf_freq"
    SUP_FREQ      = "sup_freq"
    MODE          = "mode"
    INF_BAND      = "inf_band"
    SUP_BAND      = "sup_band"
    LOCATION      = "location"
    URL           = "url"
    DESCRIPTION   = "description"
    MODULATION    = "modulation"
    CATEGORY_CODE = "category_code"
    ACF           = "acf"
    WIKI_CLICKED  = "url_clicked"

class Database(object):
    LINK_LOC  = "https://aresvalley.com/Storage/Artemis/Database/data.zip"
    LINK_REF  = "https://aresvalley.com/Storage/Artemis/Database/data.zip.log"
    NAME      = "db.csv"
    NAMES     = (Signal.NAME,         
                 Signal.INF_FREQ,
                 Signal.SUP_FREQ,
                 Signal.MODE,
                 Signal.INF_BAND,
                 Signal.SUP_BAND,
                 Signal.LOCATION,
                 Signal.URL,
                 Signal.DESCRIPTION,
                 Signal.MODULATION,
                 Signal.CATEGORY_CODE,
                 Signal.ACF,)
    DELIMITER = "*"
    STRINGS   = (Signal.INF_FREQ,
                 Signal.SUP_FREQ,
                 Signal.MODE,
                 Signal.INF_BAND,
                 Signal.SUP_BAND,
                 Signal.CATEGORY_CODE,)
                 
ACF_DOCS           = "https://aresvalley.com/documentation/"
SEARCH_LABEL_IMG   = "search_icon.png"
VOLUME_LABEL_IMG   = "volume.png"
DATA_FOLDER        = "Data"
SPECTRA_FOLDER     = "Spectra"
SPECTRA_EXT        = ".png"
AUDIO_FOLDER       = "Audio"
ACTIVE             = "active"
INACTIVE           = "inactive"
NOT_AVAILABLE      = "spectrumnotavailable.png"
NOT_SELECTED       = "nosignalselected.png"
__Band             = namedtuple("Band", ["lower", "upper"])
__ELF              = __Band(0, 30) # Formally it is (3, 30) Hz.
__SLF              = __Band(30, 300)
__ULF              = __Band(300, 3000)
__VLF              = __Band(3000, 30000)
__LF               = __Band(30 * 10**3, 300 * 10**3)
__MF               = __Band(300 * 10 ** 3, 3000 * 10**3)
__HF               = __Band(3 * 10**6, 30 * 10**6)
__VHF              = __Band(30 * 10**6, 300 * 10**6)
__UHF              = __Band(300 * 10**6, 3000 * 10**6)
__SHF              = __Band(3 * 10**9, 30 * 10**9)
__EHF              = __Band(30 * 10**9, 300 * 10**9)
BANDS              = (__ELF, __SLF, __ULF, __VLF, __LF, __MF, __HF, __VHF, __UHF, __SHF, __EHF)
MAX_DIGITS         = 3
RANGE_SEPARATOR    = ' ÷ '
GFD_SITE           = "http://qrg.globaltuners.com/"
CONVERSION_FACTORS = {"Hz" : 1, 
                      "kHz": 1000, 
                      "MHz": 1000000, 
                      "GHz": 1000000000}
MODES              = {"FM": ("NFM", "WFM"),
                      "AM": (),
                      "CW": (),
                      "SK": ("FSK", "PSK", "MSK"),
                      "SB": ("LSB", "USB", "DSB"),
                      "Chirp Spread Spectrum": (),
                      "FHSS-TDM": (),
                      "RAW": (),
                      "SC-FDMA": (),}
APPLY              = "Apply"
REMOVE             = "Remove"
UNKNOWN            = "N/A"
MODULATIONS        = ("8VSB",
                      "AFSK",
                      "AM",
                      "BFSK",
                      "C4FM",
                      "CDMA",
                      "COFDM",
                      "CW",
                      "FFSK",
                      "FM",
                      "FMCW",
                      "FMOP",
                      "FSK",
                      "GFSK",
                      "GMSK",
                      "IFK",
                      "MFSK",
                      "MSK",
                      "OFDM",
                      "OOK",
                      "PAM",
                      "PPM",
                      "PSK",
                      "QAM",
                      "TDMA",)
LOCATIONS          = (UNKNOWN,
                      "Australia",
                      "Canada",
                      "Central Europe",
                      "China",
                      "Cyprus",
                      "Eastern Europe",
                      "Europe",
                      "Europe, japan and Asia",
                      "Exmouth, Australia",
                      "Finland",
                      "France",
                      "Germany",
                      "Home Base Mobile , AL",
                      "Hungary",
                      "Iran",
                      "Israel",
                      "Japan",
                      "LaMour, North Dakota",
                      "Lualualei, Hawaii",
                      "North America",
                      "North Korea",
                      "Poland",
                      "Romania",
                      "Ruda, Sweden",
                      "UK",
                      "United Kingdom",
                      "United States",
                      "Varberg, Sweden",
                      "World Wide",
                      "Worldwide",)