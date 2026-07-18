import locale
import sys

from PySide6.QtCore import qVersion, QCoreApplication


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


class _Messages:
    """ Container class for messages to be displayed """
    # Type
    DIALOG_TYPE_INFO            = 'info'
    DIALOG_TYPE_QUEST           = 'question'
    DIALOG_TYPE_WARN            = 'warn'
    DIALOG_TYPE_ERROR           = 'error'

    # Titles
    @property
    def GENERIC_SUCCESS(self):
        return QCoreApplication.translate("Messages", "Success!")

    @property
    def GENERIC_ERROR(self):
        return QCoreApplication.translate("Messages", "Something went wrong!")

    @property
    def NO_DB_DETECTED(self):
        return QCoreApplication.translate("Messages", "No SigID database detected...")

    @property
    def NO_CONNECTION(self):
        return QCoreApplication.translate("Messages", "Connection Error!")

    @property
    def UP_TO_DATE(self):
        return QCoreApplication.translate("Messages", "You're up to date!")

    @property
    def DB_NEW_VER(self):
        return QCoreApplication.translate("Messages", "New SigID DB version available!")

    @property
    def ART_NEW_VER(self):
        return QCoreApplication.translate("Messages", "New Artemis version available!")

    @property
    def DB_CORRUPTED(self):
        return QCoreApplication.translate("Messages", "Database Corruption Detected")

    # Messages
    @property
    def DB_CREATION_SUCCESS_MSG(self):
        return QCoreApplication.translate("Messages", "The new database has been created succesfully.")

    @property
    def GENERIC_ERROR_MSG(self):
        return QCoreApplication.translate("Messages", "An error occurred during the process. Details: {}")

    @property
    def IMPORTING_SUCCESS_MSG(self):
        return QCoreApplication.translate("Messages", "Database importing has been succesfully completed!")

    @property
    def EXPORTING_SUCCESS_MSG(self):
        return QCoreApplication.translate("Messages", "Database exporting has been succesfully completed!")

    @property
    def FILE_NOT_FOUND_ERR_MSG(self):
        return QCoreApplication.translate("Messages", "The file you are trying to access cannot be located. This may be because the file has been moved or deleted.")

    @property
    def NO_DB_DETECTED_MSG(self):
        return QCoreApplication.translate("Messages", "Do you want to download it now?")

    @property
    def NO_CONNECTION_MSG(self):
        return QCoreApplication.translate("Messages", "Unable to check for updates. It appears that there is a problem with your internet connection. Please check your network settings and try again later. {}")

    @property
    def UP_TO_DATE_MSG(self):
        return QCoreApplication.translate("Messages", "The latest version of Artemis and SigID wiki is installed on your computer.")

    @property
    def DB_NEW_VER_MSG(self):
        return QCoreApplication.translate("Messages", "A new version of the database ({}) is available for download. Download now?")

    @property
    def ART_NEW_VER_MANUAL_MSG(self):
        return QCoreApplication.translate("Messages", "A new version of Artemis ({}) is available for download. Check GitHub page now?")

    @property
    def ART_NEW_VER_AUTO_MSG(self):
        return QCoreApplication.translate("Messages", "A new version of Artemis ({}) is available for download. Update Artemis now?")

    @property
    def DB_CORRUPTED_MSG(self):
        return QCoreApplication.translate("Messages", "Downloaded data corrupted or invalid. Please retry.")

    @property
    def DB_DOWNLOAD_SUCCESS_MSG(self):
        return QCoreApplication.translate("Messages", "The database has been successfully downloaded and is now being loaded.")

Messages = _Messages()
