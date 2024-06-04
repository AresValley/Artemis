import os
import sqlite3

from PySide6.QtCore import QUrl
from operator import itemgetter
from datetime import datetime
from contextlib import closing

from artemis.utils.constants import Query, Constants
from artemis.utils.path_utils import DATA_DIR
from artemis.utils.generic_utils import format_frequency


class Database():
    """ General superclass for SQLite DB manipulation.
        Foreign keys are activated (otherwise disabled by default for compatibility purposes)
    """
    def __init__(self, sql_path):
        self.sql_path = sql_path

    def execute(self, query, parameters=None, last_rowid=False):
        """ Open a connection, execute the given query with optional parameters and close the connection. 
            In the case of a SELECT query, returns the results as a fetchall().
            If last_rowid == True, this function returns a tuple with the result of the fetchall() and
            the latest modified row id of the current connection.
        """
        with closing(sqlite3.connect(self.sql_path, check_same_thread=False)) as conn:
            conn.execute('PRAGMA foreign_keys = ON;')

            curs = conn.cursor()

            if parameters:
                curs.execute(query, parameters)
            else:
                curs.execute(query)

            conn.commit()

            if last_rowid:
                result = (curs.fetchall(), curs.lastrowid)
            else:
                result = curs.fetchall()

        return result

################################## MARK: >>> DATABASE <<<

class ArtemisDatabase(Database):
    """ General CRUD class for SQLite DB manipulation.
        Foreign keys are activated (otherwise disabled by default for compatibility purposes) 
    """

    def __init__(self, db_dir_name):
        self.db_dir_name = db_dir_name
        self.db_dir = DATA_DIR / db_dir_name
        self.sql_path = self.db_dir / Constants.SQL_NAME
        self.media_dir = self.db_dir / 'media'
        super().__init__(self.sql_path)
        
        self.name = None
        self.date = None
        self.version = None
        self.editable = None

        self.all_signals = None
        self.all_modulation = None
        self.all_location = None
        self.all_category_labels = None

        self.filtered_signals = None
        
        self.stats = {}


    def load(self):
        self._select_info()
        self._select_all()
        self._select_all_modulation()
        self._select_all_location()
        self._select_all_category_labels()
        self._select_stats()


    def _select_info(self):
        """ Load the DB meta INFO from the table 'info'
        """
        result = self.execute(Query.SELECT_INFO)[0]
        self.name = result[0]
        self.date = result[1]
        self.version = result[2]
        self.editable = result[3]


    def _select_all(self):
        """ Load a list of tuple for all signals. Each tuple (representing a signal)
            contains the SIG_ID and the NAME of the signal
        """
        self.all_signals = self.execute(Query.SELECT_ALL_SIGNALS)
        keys = ('SIG_ID', 'name')
        result = [dict(zip(keys, values)) for values in self.all_signals]
        self.all_signals = result


    def _select_all_modulation(self):
        self.all_modulation = self.execute(Query.SELECT_ALL_MODULATION)
        self.all_modulation = [{'value': item[0]} for item in self.all_modulation]


    def _select_all_location(self):
        self.all_location = self.execute(Query.SELECT_ALL_LOCATION)
        self.all_location = [{'value': item[0]} for item in self.all_location]


    def _select_all_category_labels(self):
        self.all_category_labels = self.execute(Query.SELECT_ALL_CAT_LABELS)
        self.all_category_labels = [{'clb_id': item[0], 'value': item[1]} for item in self.all_category_labels]


    def _select_stats(self):
        tot_docs = self.execute(Query.SELECT_STAT_DOCS)[0][0]
        tot_images = self.execute(Query.SELECT_STAT_IMAGES)[0][0]
        tot_audio = self.execute(Query.SELECT_STAT_AUDIO)[0][0]

        self.stats['documents'] = tot_docs
        self.stats['images'] = tot_images
        self.stats['audio'] = tot_audio
        self.stats['signals'] = len(self.all_signals)


    def select_by_filter(self, filter_query):
        matching_sig_ids = self.execute(filter_query)
        sig_ids = ",".join(str(num[0]) for num in matching_sig_ids)

        self.all_signals = self.execute(Query.SELECT_SIG_ID.format(sig_ids))
        keys = ('SIG_ID', 'name')
        result = [dict(zip(keys, values)) for values in self.all_signals]
        self.all_signals = result


    def create(self, name):
        """ Create new db in the data folder.
            The name of folder containing the new db has a unique id as name (db_dir_name).
        """
        meta = [name, datetime.now(), 0, 0]
        os.makedirs(self.db_dir)
        os.makedirs(self.media_dir)

        self.execute(Query.CREATE_INFO)
        self.execute(Query.INSERT_INFO, meta)
        self.execute(Query.CREATE_SIGNALS)
        self.execute(Query.CREATE_CATEGORY)
        self.execute(Query.CREATE_CATEGORY_LABELS)
        self.execute(Query.CREATE_FREQUENCY)
        self.execute(Query.CREATE_BANDWIDTH)
        self.execute(Query.CREATE_MODULATION)
        self.execute(Query.CREATE_MODE)
        self.execute(Query.CREATE_LOCATION)
        self.execute(Query.CREATE_ACF)
        self.execute(Query.CREATE_DOCUMENTS)

        self.execute(Query.CREATE_VIEW_FREQ)
        self.execute(Query.CREATE_VIEW_BAND)


    def rename(self, name):
        self.execute(Query.RENAME_DB, [name])


    def insert_category_label(self, value):
        self.execute(Query.INSERT_CATEGORY_LABEL, [value])


    def update_category_label(self, clb_id, value):
        self.execute(Query.UPDATE_CATEGORY_LABEL, [value, clb_id])


    def delete_category_label(self, clb_id):
        self.execute(Query.DELETE_CATEGORY_LABEL, [clb_id])

################################## MARK: >>> SIGNAL <<<

class ArtemisSignal():
    """ Main class of the object signal
    """

    def __init__(self, loaded_db):
        self.db = loaded_db

        self.sig_id = None
        self.name = None
        self.description = None
        self.url = None
        self.category = None
        self.frequency = None
        self.bandwidth = None
        self.modulation = None
        self.mode = None
        self.location = None
        self.acf = None
        
        self.documents = None
        self.spectrum_path = None
        self.audio_path = None


    def load(self, sig_id):
        self.sig_id = sig_id
        self._select_signals()
        self._select_category()
        self._select_frequency()
        self._select_bandwidth()
        self._select_modulation()
        self._select_mode()
        self._select_location()
        self._select_acf()
        self.select_documents()


    def generate_dic(self):
        dic = {
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'category': self.category,
            'frequency': self.frequency,
            'bandwidth': self.bandwidth,
            'modulation': self.modulation,
            'mode': self.mode,
            'location': self.location,
            'acf': self.acf,
            'spectrum_path': self.spectrum_path,
            'audio_path': self.audio_path,
            'all_category': self.db.all_category_labels
        }
        return dic


################################## MARK: SELECT Methods


    def _select_signals(self):
        signal = self.db.execute(Query.SELECT_SIGNAL, [self.sig_id])[0]
        self.name = signal[0]
        self.description = signal[1]
        self.url = signal[2]


    def _select_category(self):
        self.category = self.db.execute(Query.SELECT_CATEGORY, [self.sig_id])
        self.category = [list(x) for x in self.category]


    def _select_frequency(self):
        result = self.db.execute(Query.SELECT_FREQUENCY, [self.sig_id])
        sorted_list = sorted(result, key=itemgetter(1))
        self.frequency = [list(x) + [format_frequency(x[1])] for x in sorted_list]


    def _select_bandwidth(self):
        result = self.db.execute(Query.SELECT_BANDWIDTH, [self.sig_id])
        sorted_list = sorted(result, key=itemgetter(1))
        self.bandwidth = [list(x) + [format_frequency(x[1])] for x in sorted_list]


    def _select_acf(self):
        self.acf = self.db.execute(Query.SELECT_ACF, [self.sig_id])
        self.acf = [list(x) for x in self.acf]


    def _select_modulation(self):
        self.modulation = self.db.execute(Query.SELECT_MODULATION, [self.sig_id])
        self.modulation = [list(x) for x in self.modulation]


    def _select_mode(self):
        self.mode = self.db.execute(Query.SELECT_MODE, [self.sig_id])
        self.mode = [list(x) for x in self.mode]


    def _select_location(self):
        self.location = self.db.execute(Query.SELECT_LOCATION, [self.sig_id])
        self.location = [list(x) for x in self.location]


    def select_documents(self):
        self.documents = self.db.execute(Query.SELECT_DOCUMENTS, [self.sig_id])

        default_spectrum = [doc for doc in self.documents if doc[4] == 'Image' and doc[5] == 1]
        default_audio = [doc for doc in self.documents if doc[4] == 'Audio' and doc[5] == 1]

        if default_spectrum != []:
            default_spectrum_filename = '{}.{}'.format(str(default_spectrum[0][0]), default_spectrum[0][1])
            self.spectrum_path = self.db.media_dir / default_spectrum_filename
            self.spectrum_path = QUrl.fromLocalFile(self.spectrum_path.resolve())
        else:
            self.spectrum_path = 'qrc:///images/spectrum_not_available.svg'

        if default_audio != []:
            default_audio_filename = '{}.{}'.format(str(default_audio[0][0]), default_audio[0][1])
            self.audio_path = self.db.media_dir / default_audio_filename
            self.audio_path = QUrl.fromLocalFile(self.audio_path.resolve())
        else:
            self.audio_path = ''


################################## MARK: UPDATE Methods


    def update_signal(self, sig_id, value, description):
        self.db.execute(Query.UPDATE_SIGNAL, [value, description, sig_id])


    def update_frequency(self, freq_id, value, description):
        self.db.execute(Query.UPDATE_FREQUENCY, [value, description, freq_id])


    def update_bandwidth(self, band_id, value, description):
        self.db.execute(Query.UPDATE_BANDWIDTH, [value, description, band_id])


    def update_modulation(self, modu_id, value, description):
        self.db.execute(Query.UPDATE_MODULATION, [value, description, modu_id])


    def update_mode(self, mode_id, value, description):
        self.db.execute(Query.UPDATE_MODE, [value, description, mode_id])


    def update_acf(self, acf_id, value, description):
        self.db.execute(Query.UPDATE_ACF, [value, description, acf_id])


    def update_location(self, loc_id, value, description):
        self.db.execute(Query.UPDATE_LOCATION, [value, description, loc_id])


    def update_documents(self, doc_id, name, description, type, is_preview):
            self.db.execute(Query.UPDATE_DOCUMENTS, [name, description, type, is_preview, doc_id])


################################## MARK: INSERT Methods


    def insert_signal(self, value, description):
        self.db.execute(Query.INSERT_SIGNAL, [value, description])


    def insert_frequency(self, value, description):
        self.db.execute(Query.INSERT_FREQUENCY, [self.sig_id, value, description])


    def insert_bandwidth(self, value, description):
        self.db.execute(Query.INSERT_BANDWIDTH, [self.sig_id,value, description])


    def insert_modulation(self, value, description):
        self.db.execute(Query.INSERT_MODULATION, [self.sig_id,value, description])


    def insert_mode(self, value, description):
        self.db.execute(Query.INSERT_MODE, [self.sig_id,value, description])


    def insert_acf(self, value, description):
        self.db.execute(Query.INSERT_ACF, [self.sig_id,value, description])


    def insert_location(self, value, description):
        self.db.execute(Query.INSERT_LOCATION, [self.sig_id,value, description])


    def insert_category(self, clb_id):
        self.db.execute(Query.INSERT_CATEGORY, [self.sig_id, clb_id])


    def insert_document(self, doc_lst):
        row_id = self.db.execute(Query.INSERT_DOCUMENTS, [self.sig_id] + doc_lst[1:], True)[1]
        return row_id


################################## MARK: DELETE Methods


    def delete_signal(self):
        self.db.execute(Query.DELETE_SIGNAL, [self.sig_id])


    def delete_frequency(self, freq_id):
        self.db.execute(Query.DELETE_FREQUENCY, [freq_id])


    def delete_bandwidth(self, band_id):
        self.db.execute(Query.DELETE_BANDWIDTH, [band_id])


    def delete_modulation(self, modu_id):
        self.db.execute(Query.DELETE_MODULATION, [modu_id])


    def delete_mode(self, mode_id):
        self.db.execute(Query.DELETE_MODE, [mode_id])


    def delete_acf(self, acf_id):
        self.db.execute(Query.DELETE_ACF, [acf_id])


    def delete_location(self, loc_id):
        self.db.execute(Query.DELETE_LOCATION, [loc_id])


    def delete_document(self, doc_id):
        self.db.execute(Query.DELETE_DOCUMENT, [doc_id])


    def delete_category(self, cat_id):
        self.db.execute(Query.DELETE_CATEGORY, [cat_id])
