from collections import namedtuple
from enum import Enum, auto
import os.path


class Ftype:
    """Container class to differentiate between frequency and band.

    used in reset_fb_filters.
    """

    FREQ = "freq"
    BAND = "band"


class GfdType(Enum):
    """Enum class to differentiate the possible GFD search criterias."""

    FREQ = auto()
    LOC  = auto()


class ChecksumWhat(Enum):
    """Enum class to distinguish the object you want to verify the checksum."""

    FOLDER = auto()
    DB = auto()


class Messages:
    """Container class for messages to be displayed."""

    DB_UP_TO_DATE            = "Already up to date"
    DB_UP_TO_DATE_MSG        = "No newer version to download."
    DB_NEW_VER               = "New version available"
    DB_NEW_VER_MSG           = "A new version of the database is available for download."
    NO_DB_AVAIL              = "No database detected."
    NO_DB                    = "No database"
    DOWNLOAD_NOW_QUESTION    = "Do you want to download it now?"
    DOWNLOAD_ANYWAY_QUESTION = "Do you want to download it anyway?"
    NO_CONNECTION            = "No connection"
    NO_CONNECTION_MSG        = "Unable to establish an internet connection."
    BAD_DOWNLOAD             = "Something went wrong"
    BAD_DOWNLOAD_MSG         = "Something went wrong with the downaload.\nCheck your internet connection and try again."


class Signal:
    """Container class for the signal property names."""

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


class Database:
    """Container class for the database-related constants."""

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
                 Signal.ACF)
    DELIMITER = "*"
    STRINGS   = (Signal.INF_FREQ,
                 Signal.SUP_FREQ,
                 Signal.MODE,
                 Signal.INF_BAND,
                 Signal.SUP_BAND,
                 Signal.CATEGORY_CODE)


class ForecastColors:
    """Container class for the forecast labels colors."""
    WARNING_COLOR = "#F95423"
    KP9_COLOR     = "#FFCCCB"
    KP8_COLOR     = "#FFCC9A"
    KP7_COLOR     = "#FFFECD"
    KP6_COLOR     = "#CDFFCC"
    KP5_COLOR     = "#BEE3FE"


class Constants:
    """Container class for several contants of the software."""

    CLICK_TO_UPDATE_STR     = "Click to update"
    SIGIDWIKI               = "https://www.sigidwiki.com/wiki/Signal_Identification_Guide"
    ADD_SIGNAL_LINK         = "https://www.sigidwiki.com/index.php/Special:FormEdit/Signal/?preload=Signal_Identification_Wiki:Signal_form_preload_text"
    FORUM_LINK              = "https://aresvalley.com/community/"
    ARESVALLEY_LINK         = "https://aresvalley.com/"
    RTL_SDL_LINK            = "https://www.rtl-sdr.com/"
    UPDATING_STR            = "Updating..."
    ACF_DOCS                = "https://aresvalley.com/documentation/"
    FORECAST_PROBABILITIES  = "https://services.swpc.noaa.gov/text/sgarf.txt"
    SPACE_WEATHER_XRAY      = "https://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt"
    SPACE_WEATHER_PROT_EL   = "https://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt"
    SPACE_WEATHER_AK_INDEX  = "https://services.swpc.noaa.gov/text/wwv.txt"
    SPACE_WEATHER_SGAS      = "https://services.swpc.noaa.gov/text/sgas.txt"
    SPACE_WEATHER_GEO_STORM = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    SPACE_WEATHER_INFO      = "https://www.swpc.noaa.gov/sites/default/files/images/NOAAscales.pdf"
    SPACE_WEATHER_IMGS      = ["http://www.mmmonvhf.de/eme/eme.png",
                               "http://www.mmmonvhf.de/ms/ms.png",
                               "http://www.mmmonvhf.de/es/es.png",
                               "http://www.mmmonvhf.de/solar/solar.png",
                               "http://amunters.home.xs4all.nl/eskip50status.gif",
                               "http://amunters.home.xs4all.nl/eskip70status.gif",
                               "http://amunters.home.xs4all.nl/eskipstatus.gif",
                               "https://amunters.home.xs4all.nl/eskipstatusNA.gif",
                               "https://amunters.home.xs4all.nl/aurorastatus.gif"]
    SEARCH_LABEL_IMG        = "search_icon.png"
    VOLUME_LABEL_IMG        = "volume.png"
    DATA_FOLDER             = "Data"
    SPECTRA_FOLDER          = "Spectra"
    SPECTRA_EXT             = ".png"
    AUDIO_FOLDER            = "Audio"
    ACTIVE                  = "active"
    INACTIVE                = "inactive"
    LABEL_ON_COLOR          = "on"
    LABEL_OFF_COLOR         = "off"
    TEXT_COLOR              = "text"
    __Band                  = namedtuple("Band", ["lower", "upper"])
    __ELF                   = __Band(0, 30) # Formally it is (3, 30) Hz.
    __SLF                   = __Band(30, 300)
    __ULF                   = __Band(300, 3000)
    __VLF                   = __Band(3000, 30000)
    __LF                    = __Band(30 * 10**3, 300 * 10**3)
    __MF                    = __Band(300 * 10 ** 3, 3000 * 10**3)
    __HF                    = __Band(3 * 10**6, 30 * 10**6)
    __VHF                   = __Band(30 * 10**6, 300 * 10**6)
    __UHF                   = __Band(300 * 10**6, 3000 * 10**6)
    __SHF                   = __Band(3 * 10**9, 30 * 10**9)
    __EHF                   = __Band(30 * 10**9, 300 * 10**9)
    BANDS                   = (__ELF, __SLF, __ULF, __VLF, __LF, __MF, __HF, __VHF, __UHF, __SHF, __EHF)
    MAX_DIGITS              = 3
    RANGE_SEPARATOR         = ' ÷ '
    GFD_SITE                = "http://qrg.globaltuners.com/"
    CONVERSION_FACTORS      = {"Hz" : 1,
                               "kHz": 1000,
                               "MHz": 1000000,
                               "GHz": 1000000000}
    MODES                   = {"FM": ("NFM", "WFM"),
                               "AM": (),
                               "CW": (),
                               "SK": ("FSK", "PSK", "MSK"),
                               "SB": ("LSB", "USB", "DSB"),
                               "Chirp Spread Spectrum": (),
                               "FHSS-TDM": (),
                               "RAW": (),
                               "SC-FDMA": ()}
    APPLY                   = "Apply"
    REMOVE                  = "Remove"
    UNKNOWN                 = "N/A"
    EXTRACTING_MSG          = "Extracting..."
    EXTRACTING_CODE         = -1
    NOT_AVAILABLE           = "spectrumnotavailable.png"
    NOT_SELECTED            = "nosignalselected.png"
    DEFAULT_IMGS_FOLDER     = os.path.join(":", "pics", "default_pics")
    DEFAULT_NOT_SELECTED    = os.path.join(DEFAULT_IMGS_FOLDER, NOT_SELECTED)
    DEFAULT_NOT_AVAILABLE   = os.path.join(DEFAULT_IMGS_FOLDER, NOT_AVAILABLE)
