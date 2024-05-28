from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

from artemis.utils.path_utils import *
from artemis.utils.generic_utils import *


class UIcategoryeditor(QObject):
    # Python > QML Signals
    show_ui = Signal()
    load = Signal(list)


    def __init__(self, parent):
        super().__init__()

        self._parent = parent

        self._engine = QQmlApplicationEngine()
        self._engine.load('qrc:/ui/CategoryEditor.qml')
        self._window = self._engine.rootObjects()[0]

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.saveParam.connect(self.save)
        self._window.deleteParam.connect(self.delete)

        # Python > QML connections
        self.show_ui.connect(self._window.show)
        self.load.connect(self._window.loadList)


    def load_cateditor_ui(self):
        """ Load the list with existing category tags and show the UI
        """
        all_cat = self._parent.loaded_db.all_category_labels
        self.load.emit(all_cat)
        self.show_ui.emit()


    @Slot(list, bool)
    def save(self, data, is_new):
        """ Save new category tag or update the existing ones.
        """
        data = data.toVariant()

        if is_new:
            self._parent.loaded_db.insert_category_label(data[0])
        else:
            self._parent.loaded_db.update_category_label(data[1], data[0])

        self._parent.load_db(self._parent.loaded_db.db_dir_name)
        self.load_cateditor_ui()


    @Slot(int)
    def delete(self, clb_id):
        """ Delete a database category tag.
            All the entries in the documents table are automatically beign deleted due to 
            foreign-key cascade propagation
        """
        self._parent.loaded_db.delete_category_label(clb_id)
        self._parent.load_db(self._parent.loaded_db.db_dir_name)
        self.load_cateditor_ui()
