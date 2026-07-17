import locale
import sys

from PySide6.QtCore import qVersion


class Constants():
    """ Container class for several constants of the software """

    APPLICATION_NAME            = 'Artemis'
    ORGANIZATION_NAME           = 'AresValley'
    ORGANIZATION_DOMAIN         = 'aresvalley.com'
    APPLICATION_VERSION         = '4.1.5'

    SQL_NAME                    = 'data.sqlite'

    LATEST_VERSION_URL          = 'https://raw.githubusercontent.com/AresValley/Artemis/master/config/release-info.json'
    POSEIDON_REPORT_URL         = 'https://www.aresvalley.com/poseidon_engine/data.json'

    DEFAULT_ENCODING            = 'utf-8'
    SYSTEM_LANGUAGE             = 'en_US' # locale.getdefaultlocale()[0]
    PYTHON_VERSION              = '.'.join(str(v) for v in sys.version_info[:3])
    QT_VERSION                  = qVersion()


class Messages:
    """ Container class for messages to be displayed """
    # Type
    DIALOG_TYPE_INFO            = 'info'
    DIALOG_TYPE_QUEST           = 'question'
    DIALOG_TYPE_WARN            = 'warn'
    DIALOG_TYPE_ERROR           = 'error'

    # Titles
    GENERIC_SUCCESS             = "Success!"
    GENERIC_ERROR               = "Something went wrong!"
    NO_DB_DETECTED              = "No SigID database detected..."
    NO_CONNECTION               = "Connection Error!"
    UP_TO_DATE                  = "You're up to date!"
    DB_NEW_VER                  = "New SigID DB version available!"
    ART_NEW_VER                 = "New Artemis version available!"
    DB_CORRUPTED                = "Database Corruption Detected"

    # Messages
    DB_CREATION_SUCCESS_MSG     = "The new database has been created succesfully."
    GENERIC_ERROR_MSG           = "An error occurred during the process. Details: {}"
    IMPORTING_SUCCESS_MSG       = "Database importing has been succesfully completed!"
    EXPORTING_SUCCESS_MSG       = "Database exporting has been succesfully completed!"
    FILE_NOT_FOUND_ERR_MSG      = "The file you are trying to access cannot be located. This may be because the file has been moved or deleted."
    NO_DB_DETECTED_MSG          = "Do you want to download it now?"
    NO_CONNECTION_MSG           = "Unable to check for updates. It appears that there is a problem with your internet connection. Please check your network settings and try again later. {}"
    UP_TO_DATE_MSG              = "The latest version of Artemis and SigID wiki is installed on your computer."
    DB_NEW_VER_MSG              = "A new version of the database ({}) is available for download. Download now?"
    ART_NEW_VER_MANUAL_MSG      = "A new version of Artemis ({}) is available for download. Check GitHub page now?"
    ART_NEW_VER_AUTO_MSG        = "A new version of Artemis ({}) is available for download. Update Artemis now?"
    DB_CORRUPTED_MSG            = "Downloaded data corrupted or invalid. Please retry."
    DB_DOWNLOAD_SUCCESS_MSG     = "The database has been successfully downloaded and is now being loaded."
