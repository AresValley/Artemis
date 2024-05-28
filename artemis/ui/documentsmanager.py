from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

from artemis.utils.path_utils import *
from artemis.utils.generic_utils import *
from artemis.utils.sys_utils import *


class UIdocumentsmanager(QObject):
    # Python > QML Signals
    show_ui = Signal()
    close_ui = Signal()
    populate_documents_list = Signal(list)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/DocumentsManager.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.saveNewDoc.connect(self.save_new_doc)
        self._window.deleteDoc.connect(self.delete_doc)
        self._window.updateDoc.connect(self.update_doc)
        self._window.openDoc.connect(self.open_doc)


        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.close_ui.connect(self._window.close)
        self.populate_documents_list.connect(self._window.loadList)


    def load_documentsmanager_ui(self):
        self.load_documents_list()
        self.show_ui.emit()


    def load_documents_list(self):
        """ Load the documents of the selected signal and populate the documents list
        """
        self._parent.loaded_sig.select_documents()
        all_documents = self._parent.loaded_sig.documents
        
        keys = (
            'doc_id',
            'extension',
            'name',
            'description',
            'type',
            'preview'
        )
        
        doc_lst = [dict(zip(keys, values)) for values in all_documents]
        self.populate_documents_list.emit(doc_lst)


    @Slot(list)
    def save_new_doc(self, doc_lst):
        """ Save the new document (identified by the DOC_ID = -1) and reload the document list.
            doc_param contains all the details of the new documents. 
        """
        doc_param = doc_lst.toVariant()
        file_extension = os.path.splitext(doc_param[0])[1][1:]

        doc_id = self._parent.loaded_sig.insert_document([
            -1,
            file_extension,
            doc_param[1],
            doc_param[2],
            doc_param[3],
            0
        ])

        local_file_name = '{}.{}'.format(str(doc_id), file_extension)
        origin_path = normalize_dialog_path(doc_param[0])
        copy_file(origin_path, self._parent.loaded_db.media_dir / local_file_name)
        self.load_documents_list()


    @Slot(list)
    def update_doc(self, doc_lst):
        """ Update the details of the existent document
        """
        doc_list = doc_lst.toVariant()
        for doc in doc_list:
            self._parent.loaded_sig.update_documents(doc[0], doc[1], doc[2], doc[3], doc[4])
        self.load_documents_list()


    @Slot(str, str)
    def open_doc(self, doc_id, extension):
        """ Open the selected document with the proper system application (if any)
        """
        try:
            open_file(self._parent.loaded_db.media_dir / '{}.{}'.format(doc_id, extension))
        except Exception as e:
            self.close_ui.emit()
            self._parent.dialog_popup(
                Messages.DIALOG_TYPE_ERROR,
                Messages.GENERIC_ERROR,
                str(e)
            )


    @Slot(str, str, str, bool)
    def delete_doc(self, doc_id, doc_extension, doc_type, doc_preview):
        """ Delete the selected document
        """
        doc_file_name = '{}.{}'.format(doc_id, doc_extension)
        doc_file_path = self._parent.loaded_db.media_dir / doc_file_name
        
        self._parent.loaded_sig.delete_document(doc_id)
        
        if doc_preview:
            if doc_type == 'Audio':
                self._parent.lock_audio_player.emit()

        delete_file(doc_file_path)
        self.load_documents_list()
