from collections import namedtuple
from enum import Enum, auto
import os.path
from executable_utilities import get_executable_path


__BASE_FOLDER__ = get_executable_path()


class SupportedOs:
    """Supported operating systems."""
    WINDOWS = "windows"
    LINUX   = "linux"
    MAC     = "mac"
    RASPBIAN = "raspberry"


class Ftype:
    """Container class to differentiate between frequency and band."""

    FREQ = "freq"
    BAND = "band"


class GfdType(Enum):
    """Enum class to differentiate the possible GFD search criterias."""

    FREQ = auto()
    LOC  = auto()


class DownloadTarget(Enum):
    """Enum class to distinguish the object being downloaded."""

    DATA_FOLDER = auto()
    DB          = auto()
    SOFTWARE    = auto()
    UPDATER     = auto()


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
                 Signal.CATEGORY_CODE,
                 Signal.ACF,)


class ForecastColors:
    """Container class for the forecast labels colors."""

    WARNING_COLOR = "#F95423"
    KP9_COLOR     = "#FFCCCB"
    KP8_COLOR     = "#FFCC9A"
    KP7_COLOR     = "#FFFECD"
    KP6_COLOR     = "#CDFFCC"
    KP5_COLOR     = "#BEE3FE"


_Band = namedtuple("Band", ["lower", "upper"])


class Constants:
    """Container class for several constants of the software."""

    EXECUTABLE_NAME         = os.path.join(__BASE_FOLDER__, "Artemis")
    UPDATER_SOFTWARE        = os.path.join(__BASE_FOLDER__, "_ArtemisUpdater")
    CLICK_TO_UPDATE_STR     = "Click to update"
    VERSION_LINK            = "https://aresvalley.com/Storage/Artemis/Package/latest_versions.json"
    SIGIDWIKI               = "https://www.sigidwiki.com/wiki/Signal_Identification_Guide"
    ADD_SIGNAL_LINK         = "https://www.sigidwiki.com/index.php/Special:FormEdit/Signal/?preload=Signal_Identification_Wiki:Signal_form_preload_text"
    FORUM_LINK              = "https://aresvalley.com/community/"
    ARESVALLEY_LINK         = "https://aresvalley.com/"
    GITHUB_REPO             = "https://github.com/AresValley/Artemis"
    RTL_SDL_LINK            = "https://www.rtl-sdr.com/"
    UPDATING_STR            = "Updating..."
    ACF_DOCS                = "https://aresvalley.com/documentation/"
    FORECAST_PROBABILITIES  = "https://services.swpc.noaa.gov/text/sgarf.txt"
    SPACE_WEATHER_XRAY      = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
    SPACE_WEATHER_PROT_EL   = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json"
    SPACE_WEATHER_AK_INDEX  = "https://services.swpc.noaa.gov/text/wwv.txt"
    SPACE_WEATHER_SGAS      = "https://services.swpc.noaa.gov/text/sgas.txt"
    SPACE_WEATHER_GEO_STORM = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    SPACE_WEATHER_INFO      = "https://www.swpc.noaa.gov/sites/default/files/images/NOAAscales.pdf"
    SPACE_WEATHER_IMGS      = ["https://www.mmmonvhf.de/eme/eme.png",
                               "https://www.mmmonvhf.de/ms/ms.png",
                               "https://www.mmmonvhf.de/es/es.png",
                               "https://www.mmmonvhf.de/solar/solar.png",
                               "https://amunters.home.xs4all.nl/eskip50status.gif",
                               "https://amunters.home.xs4all.nl/eskip70status.gif",
                               "https://amunters.home.xs4all.nl/eskipstatus.gif",
                               "https://amunters.home.xs4all.nl/eskipstatusNA.gif",
                               "https://amunters.home.xs4all.nl/aurorastatus.gif"]
    SEARCH_LABEL_IMG        = "search_icon.png"
    VOLUME_LABEL_IMG        = "volume.png"
    SPECTRA_EXT             = ".png"
    ACTIVE                  = "active"
    INACTIVE                = "inactive"
    LABEL_ON_COLOR          = "on"
    LABEL_OFF_COLOR         = "off"
    TEXT_COLOR              = "text"
    _ELF                    = _Band(0, 30)  # Formally it is (3, 30) Hz.
    _SLF                    = _Band(30, 300)
    _ULF                    = _Band(300, 3000)
    _VLF                    = _Band(3000, 30000)
    _LF                     = _Band(30 * 10**3, 300 * 10**3)
    _MF                     = _Band(300 * 10 ** 3, 3000 * 10**3)
    _HF                     = _Band(3 * 10**6, 30 * 10**6)
    _VHF                    = _Band(30 * 10**6, 300 * 10**6)
    _UHF                    = _Band(300 * 10**6, 3000 * 10**6)
    _SHF                    = _Band(3 * 10**9, 30 * 10**9)
    _EHF                    = _Band(30 * 10**9, 300 * 10**9)
    BANDS                   = (_ELF, _SLF, _ULF, _VLF, _LF, _MF, _HF, _VHF, _UHF, _SHF, _EHF)
    MAX_DIGITS              = 3
    RANGE_SEPARATOR         = ' ÷ '
    GFD_SITE                = "http://qrg.globaltuners.com/"
    CONVERSION_FACTORS      = {"Hz": 1,
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
    ZERO_INITIAL_SPEED      = -1
    ZERO_FINAL_SPEED        = -2
    NOT_AVAILABLE           = "spectrumnotavailable.png"
    NOT_SELECTED            = "nosignalselected.png"
    FIELD_SEPARATOR         = ";"
    ACF_SEPARATOR           = " - "
    DATA_FOLDER             = os.path.join(__BASE_FOLDER__, "Data")
    SPECTRA_FOLDER          = os.path.join(DATA_FOLDER, "Spectra")
    AUDIO_FOLDER            = os.path.join(DATA_FOLDER, "Audio")
    DEFAULT_IMGS_FOLDER     = os.path.join(":", "pics", "default_pics")
    DEFAULT_NOT_SELECTED    = os.path.join(DEFAULT_IMGS_FOLDER, NOT_SELECTED)
    DEFAULT_NOT_AVAILABLE   = os.path.join(DEFAULT_IMGS_FOLDER, NOT_AVAILABLE)
    FONT_FILE               = os.path.join(__BASE_FOLDER__, 'font.json')
    SETTINGS_FILE           = os.path.join(__BASE_FOLDER__, "settings.json")


class Messages:
    """Container class for messages to be displayed."""

    FEATURE_NOT_AVAILABLE    = "Feature not available"
    SCRIPT_NOT_UPDATE        = "When running from source, software updates\ncannot be checked."
    UPDATES_AVAILABALE       = "Updates available"
    UPDATES_MSG              = "Do you want to install the updates now?"
    UP_TO_DATE               = "Already up to date"
    UP_TO_DATE_MSG           = "No newer version to download."
    DB_NEW_VER               = "New version available"
    DB_NEW_VER_MSG           = "A new version of the database is available for download."
    NO_DB_AVAIL              = "No database detected."
    NO_DB                    = "No database"
    DOWNLOAD_NOW_QUESTION    = "Do you want to download it now?"
    DOWNLOAD_ANYWAY_QUESTION = "Do you want to download it anyway?"
    NO_CONNECTION            = "No connection"
    NO_CONNECTION_MSG        = "Unable to establish an internet connection."
    BAD_DOWNLOAD             = "Something went wrong"
    BAD_DOWNLOAD_MSG         = "Something went wrong with the download.\nCheck your internet connection and try again."
    SLOW_CONN                = "Slow internet connection"
    SLOW_CONN_MSG            = "Your internet connection is unstable or too slow."
    NEW_VERSION_AVAILABLE    = "New software version"
    NEW_VERSION_MSG          = lambda v: f"The software version {v} is available."  # noqa: E731
    DOWNLOAD_SUGG_MSG        = "Download new version now?"
    SCREEN_UPDATE_FAIL       = "Unable to update the data"
    SCREEN_UPDATE_FAIL_MSG   = "Downloaded data currupted or invalid"


class ThemeConstants:
    """Container class for all the theme-related constants."""

    EXTENSION                 = ".qss"
    ICONS_FOLDER              = "icons"
    DEFAULT                   = "material_design_dark"
    COLORS                    = "colors.txt"
    COLOR_SEPARATOR           = "="
    DEFAULT_ACTIVE_COLOR      = "#000000"
    DEFAULT_INACTIVE_COLOR    = "#9f9f9f"
    DEFAULT_OFF_COLORS        = "#000000", "#434343"
    DEFAULT_ON_COLORS         = "#4b79a1", "#283e51"
    DEFAULT_TEXT_COLOR        = "#ffffff"
    THEME_NOT_FOUND           = "Theme not found"
    MISSING_THEME             = "Missing theme folder."
    MISSING_THEME_FOLDER      = "Themes folder not found.\nOnly the basic theme is available."
    THEME_FOLDER_NOT_FOUND    = "Themes folder not found"
    FOLDER                    = os.path.join(__BASE_FOLDER__, "themes")
    DEFAULT_ICONS_PATH        = os.path.join(FOLDER, DEFAULT, ICONS_FOLDER)
    DEFAULT_SEARCH_LABEL_PATH = os.path.join(DEFAULT_ICONS_PATH, Constants.SEARCH_LABEL_IMG)
    DEFAULT_VOLUME_LABEL_PATH = os.path.join(DEFAULT_ICONS_PATH, Constants.VOLUME_LABEL_IMG)
    DEFAULT_THEME_PATH        = os.path.join(FOLDER, DEFAULT)
