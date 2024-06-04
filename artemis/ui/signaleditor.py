from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

from artemis.utils.path_utils import *
from artemis.utils.generic_utils import *
from artemis.utils.sql_utils import ArtemisSignal
from artemis.utils.sys_utils import delete_file


class UIsignaleditor(QObject):
    # Python > QML Signals
    show_ui = Signal()
    load = Signal(str, list, bool)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/SignalEditor.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.saveParam.connect(self.save)
        self._window.deleteParam.connect(self.delete)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.load.connect(self._window.load)


    def load_signaleditor_ui(self, param_type, sig_param, is_new):
        """ Load all the details of the selected signal

        Args:
            param_type (str): Signal, Frequency, Bandwidth, Modulation, Mode,
                ACF, Location
            sig_param (list): a list formed as [id, value, description]
            is_new (bool): If true, the windows open in an empty state ready to 
                be compiled by the user. If false, the windows will open all the 
                current parameter for the loaded signal, for editing or deleting purposes.
        """
        if param_type == 'Signal' and not is_new:
            sig_param = [
                self._parent.loaded_sig.sig_id,
                self._parent.loaded_sig.name,
                self._parent.loaded_sig.description
            ]
        self.load.emit(param_type, sig_param, is_new)
        self.show_ui.emit()


    @Slot(str, list, bool)
    def save(self, param_type, data, is_new):
        """ Save new signal parameters or update the existing ones.
        """
        data = data.toVariant()

        if is_new:
            if param_type == 'Signal':
                self._parent.loaded_sig = ArtemisSignal(self._parent.loaded_db)
                self._parent.loaded_sig.insert_signal(data[1], data[2])
            elif param_type == 'Frequency':
                self._parent.loaded_sig.insert_frequency(int(data[1]), data[2])
            elif param_type == 'Bandwidth':
                self._parent.loaded_sig.insert_bandwidth(int(data[1]), data[2])
            elif param_type == 'Modulation':
                self._parent.loaded_sig.insert_modulation(data[1], data[2])        
            elif param_type == 'Mode':
                self._parent.loaded_sig.insert_mode(data[1], data[2])
            elif param_type == 'ACF':
                self._parent.loaded_sig.insert_acf(data[1], data[2])
            elif param_type == 'Location':
                self._parent.loaded_sig.insert_location(data[1], data[2])
        else:
            if param_type == 'Signal':
                self._parent.loaded_sig.update_signal(data[0], data[1], data[2])
            elif param_type == 'Frequency':
                self._parent.loaded_sig.update_frequency(data[0], int(data[1]), data[2])
            elif param_type == 'Bandwidth':
                self._parent.loaded_sig.update_bandwidth(data[0], int(data[1]), data[2])
            elif param_type == 'Modulation':
                self._parent.loaded_sig.update_modulation(data[0], data[1], data[2])        
            elif param_type == 'Mode':
                self._parent.loaded_sig.update_mode(data[0], data[1], data[2])
            elif param_type == 'ACF':
                self._parent.loaded_sig.update_acf(data[0], data[1], data[2])
            elif param_type == 'Location':
                self._parent.loaded_sig.update_location(data[0], data[1], data[2])

        self._parent.load_db(self._parent.loaded_db.db_dir_name)


    @Slot(str, int)
    def delete(self, param_type, id):
        """ Delete a signal parameter or the signal itself (with all the parameters and documents).
            All the entries in the documents table are automatically beign deleted due to 
            foreign-key cascade propagation
        """
        if param_type == 'Signal':
            self._parent.loaded_sig.delete_signal()
            self._parent.lock_audio_player.emit()
            for doc in self._parent.loaded_sig.documents:
                doc_file_name = '{}.{}'.format(str(doc[0]), doc[1])
                doc_file_path = self._parent.loaded_db.media_dir / doc_file_name
                delete_file(doc_file_path)
        elif param_type == 'Frequency':
            self._parent.loaded_sig.delete_frequency(id)
        elif param_type == 'Bandwidth':
            self._parent.loaded_sig.delete_bandwidth(id)
        elif param_type == 'Modulation':
            self._parent.loaded_sig.delete_modulation(id)        
        elif param_type == 'Mode':
            self._parent.loaded_sig.delete_mode(id)
        elif param_type == 'ACF':
            self._parent.loaded_sig.delete_acf(id)
        elif param_type == 'Location':
            self._parent.loaded_sig.delete_location(id)

        self._parent.load_db(self._parent.loaded_db.db_dir_name)
