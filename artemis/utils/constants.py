import locale
import sys

from PySide6.QtCore import qVersion


class Constants():
    """ Container class for several constants of the software """

    APPLICATION_NAME            = 'Artemis'
    ORGANIZATION_NAME           = 'AresValley'
    ORGANIZATION_DOMAIN         = 'aresvalley.com'
    APPLICATION_VERSION         = '4.0.3'

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
    ART_NEW_VER_MSG             = "A new version of Artemis ({}) is available for download. Check GitHub page now?"
    DOWNLOAD_CORRUPTED_MSG      = "Downloaded data corrupted or invalid. Please retry."


class Query():
    """ Container class for all the sqlite queries """
    
############################## SELECT

    SELECT_ALL_SIGNALS = "SELECT SIG_ID, NAME, DESCRIPTION FROM signals ORDER BY NAME ASC"
    
    SELECT_ALL_MODULATION = "SELECT DISTINCT VALUE FROM modulation ORDER BY VALUE ASC"
    
    SELECT_ALL_LOCATION = "SELECT DISTINCT VALUE FROM location ORDER BY VALUE ASC"
    
    SELECT_SIG_ID = "SELECT SIG_ID, NAME, DESCRIPTION FROM signals WHERE SIG_ID IN ({}) ORDER BY NAME ASC"

    SELECT_ALL_CAT_LABELS = "SELECT CLB_ID, VALUE FROM category_label ORDER BY VALUE ASC"
    
    SELECT_INFO = """
        SELECT
            NAME,
            DATE,
            VERSION,
            EDITABLE
        FROM info
    """

    SELECT_SIGNAL = """
        SELECT
            NAME,
            DESCRIPTION,
            URL
        FROM signals WHERE SIG_ID = ?
    """
    
    SELECT_CATEGORY = """
        SELECT
            category.CAT_ID,
            category_label.VALUE
        FROM category
        INNER JOIN category_label ON category.CLB_ID = category_label.CLB_ID
        WHERE SIG_ID = ?
    """

    SELECT_DOCUMENTS = """
        SELECT
            DOC_ID,
            EXTENSION,
            NAME,
            DESCRIPTION,
            TYPE,
            PREVIEW 
        FROM documents WHERE SIG_ID = ?
        ORDER BY TYPE ASC
    """

    SELECT_FREQUENCY = """
        SELECT
            FREQ_ID,
            VALUE,
            DESCRIPTION
        FROM frequency WHERE SIG_ID = ?
    """

    SELECT_BANDWIDTH = """
        SELECT
            BAND_ID,
            VALUE,
            DESCRIPTION
        FROM bandwidth WHERE SIG_ID = ?
    """

    SELECT_MODULATION = """
        SELECT
            MDL_ID,
            VALUE,
            DESCRIPTION
        FROM modulation WHERE SIG_ID = ?
    """

    SELECT_MODE= """
        SELECT
            MOD_ID,
            VALUE,
            DESCRIPTION
        FROM mode WHERE SIG_ID = ?
    """

    SELECT_LOCATION = """
        SELECT
            LOC_ID,
            VALUE,
            DESCRIPTION
        FROM location WHERE SIG_ID = ?
    """

    SELECT_ACF = """
        SELECT
            ACF_ID,
            VALUE,
            DESCRIPTION
        FROM acf WHERE SIG_ID = ?
    """

    SELECT_STAT_DOCS = """
        SELECT COUNT(*)
            FROM documents
    """
    
    SELECT_STAT_IMAGES = """
        SELECT COUNT(*)
            FROM documents
        WHERE type IS 'Image'
    """

    SELECT_STAT_AUDIO = """
        SELECT COUNT(*)
            FROM documents
        WHERE type IS 'Audio'
    """    

############################## CREATE

    CREATE_SIGNALS = """
        CREATE TABLE signals (
            SIG_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME        TEXT,
            DESCRIPTION TEXT,
            URL         TEXT
        )
    """

    CREATE_CATEGORY = """
        CREATE TABLE category (
            CAT_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER,
            CLB_ID      INTEGER,
            FOREIGN KEY (SIG_ID) REFERENCES signals (SIG_ID) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (CLB_ID) REFERENCES category_label (CLB_ID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """

    CREATE_CATEGORY_LABELS = """
        CREATE TABLE category_label (
            CLB_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            VALUE       TEXT
        )   
    """

    CREATE_DOCUMENTS = """
        CREATE TABLE documents (
            DOC_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER REFERENCES signals (SIG_ID) ON DELETE CASCADE,
            EXTENSION   TEXT,
            NAME        TEXT,
            DESCRIPTION TEXT,
            TYPE        TEXT,
            PREVIEW     INTEGER
        )
    """
    
    CREATE_FREQUENCY = """
        CREATE TABLE frequency (
            FREQ_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER REFERENCES signals (SIG_ID) ON DELETE CASCADE,
            VALUE       INTEGER,
            DESCRIPTION TEXT
        )    
    """
    
    CREATE_BANDWIDTH = """
        CREATE TABLE bandwidth (
            BAND_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER REFERENCES signals (SIG_ID) ON DELETE CASCADE,
            VALUE       INTEGER,
            DESCRIPTION TEXT
        )    
    """    

    CREATE_MODULATION = """
        CREATE TABLE modulation (
            MDL_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER REFERENCES signals (SIG_ID) ON DELETE CASCADE,
            VALUE       TEXT,
            DESCRIPTION TEXT
        )
    """

    CREATE_MODE = """
        CREATE TABLE mode (
            MOD_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER,
            VALUE       TEXT,
            DESCRIPTION TEXT,
            FOREIGN KEY (SIG_ID) REFERENCES signals (SIG_ID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """

    CREATE_LOCATION = """
        CREATE TABLE location (
            LOC_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER,
            VALUE       TEXT,
            DESCRIPTION TEXT,
            FOREIGN KEY (SIG_ID) REFERENCES signals (SIG_ID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """

    CREATE_ACF = """
        CREATE TABLE acf (
            ACF_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            SIG_ID      INTEGER REFERENCES signals (SIG_ID) ON DELETE CASCADE,
            VALUE       FLOAT,
            DESCRIPTION TEXT
        )    
    """     

    CREATE_INFO = """
        CREATE TABLE info (
            NAME        TEXT,
            DATE        TEXT,
            VERSION     INTEGER,
            EDITABLE    INTEGER
        )   
    """

    CREATE_VIEW_FREQ = """
        CREATE VIEW FREQ_RANGE AS
            SELECT SIG_ID,
                MIN(VALUE) AS MIN_VALUE,
                MAX(VALUE) AS MAX_VALUE
            FROM frequency
            GROUP BY SIG_ID
    """        

    CREATE_VIEW_BAND = """
        CREATE VIEW BAND_RANGE AS
            SELECT SIG_ID,
                MIN(VALUE) AS MIN_VALUE,
                MAX(VALUE) AS MAX_VALUE
            FROM bandwidth
            GROUP BY SIG_ID 
    """

############################## INSERT

    INSERT_SIGNAL = """
        INSERT INTO signals (
            NAME,
            DESCRIPTION
        ) VALUES (?,?)
    """

    INSERT_CATEGORY = """
        INSERT INTO category (
            SIG_ID,
            CLB_ID
        ) VALUES (?,?)
    """

    INSERT_CATEGORY_LABEL = """
        INSERT INTO category_label (
            VALUE
        ) VALUES (?)
    """

    INSERT_INFO = """
        INSERT INTO info (
            NAME,
            DATE,
            VERSION,
            EDITABLE
        ) VALUES (?,?,?,?)
    """

    INSERT_DOCUMENTS = """
        INSERT INTO documents (
            SIG_ID,
            EXTENSION,
            NAME,
            DESCRIPTION,
            TYPE,
            PREVIEW 
        ) VALUES (?,?,?,?,?,?)
    """

    INSERT_FREQUENCY = """
        INSERT INTO frequency (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

    INSERT_BANDWIDTH = """
        INSERT INTO bandwidth (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

    INSERT_MODULATION = """
        INSERT INTO modulation (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

    INSERT_MODE = """
        INSERT INTO mode (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

    INSERT_LOCATION = """
        INSERT INTO location (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

    INSERT_ACF = """
        INSERT INTO acf (
            SIG_ID,
            VALUE,
            DESCRIPTION
        ) VALUES (?,?,?)
    """

############################## UPDATE

    RENAME_DB = "UPDATE info SET NAME = ?"

    UPDATE_SIGNAL = """
        UPDATE signals SET
            NAME = ?,
            DESCRIPTION = ?
        WHERE SIG_ID = ?
    """

    UPDATE_CATEGORY_LABEL = """
        UPDATE category_label SET
            VALUE = ?
        WHERE CLB_ID = ?
    """

    UPDATE_FREQUENCY = """
        UPDATE frequency SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE FREQ_ID = ?
    """

    UPDATE_BANDWIDTH = """
        UPDATE bandwidth SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE BAND_ID = ?
    """

    UPDATE_ACF = """
        UPDATE acf SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE ACF_ID = ?
    """

    UPDATE_MODE = """
        UPDATE mode SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE MOD_ID = ?
    """

    UPDATE_LOCATION = """
        UPDATE location SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE LOC_ID = ?
    """

    UPDATE_MODULATION = """
        UPDATE modulation SET
            VALUE = ?,
            DESCRIPTION = ?
        WHERE MDL_ID = ?
    """

    UPDATE_DOCUMENTS = """
        UPDATE documents SET
            NAME = ?,
            DESCRIPTION = ?,
            TYPE = ?,
            PREVIEW = ?
        WHERE DOC_ID = ?
    """

############################## DELETE
    
    DELETE_SIGNAL = "DELETE FROM signals WHERE SIG_ID = ?"

    DELETE_DOCUMENT = "DELETE FROM documents WHERE DOC_ID = ?"

    DELETE_FREQUENCY = "DELETE FROM frequency WHERE FREQ_ID = ?"

    DELETE_BANDWIDTH = "DELETE FROM bandwidth WHERE BAND_ID = ?"

    DELETE_MODULATION = "DELETE FROM modulation WHERE MDL_ID = ?"
    
    DELETE_MODE = "DELETE FROM mode WHERE MOD_ID = ?"
    
    DELETE_LOCATION = "DELETE FROM location WHERE LOC_ID = ?"

    DELETE_ACF = "DELETE FROM acf WHERE ACF_ID = ?"

    DELETE_CATEGORY = "DELETE FROM category WHERE CAT_ID = ?"

    DELETE_CATEGORY_LABEL = "DELETE FROM category_label WHERE CLB_ID = ?"

############################## FILTER QUERY

    FILTER_FREQ = "SELECT SIG_ID FROM FREQ_RANGE WHERE ({} >= MIN_VALUE) AND ({} <= MAX_VALUE)"

    FILTER_BAND = "SELECT SIG_ID FROM BAND_RANGE WHERE ({} >= MIN_VALUE) AND ({} <= MAX_VALUE)"

    FILTER_ACF = "SELECT SIG_ID FROM acf WHERE ({} >= VALUE) AND ({} <= VALUE)"

    FILTER_MODULATION = "SELECT SIG_ID FROM modulation WHERE VALUE IN ({})"

    FILTER_LOCATION = "SELECT SIG_ID FROM location WHERE VALUE IN ({})"

    FILTER_CATEGORY = "SELECT SIG_ID FROM category WHERE CLB_ID IN ({})"
