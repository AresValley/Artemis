from PySide6.QtCore import QObject, Slot, Signal

from artemis.utils.generic_utils import generate_filter_query


class FiltersManager(QObject):
    # Python > QML Signals
    populate_filter_list = Signal(list)

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self._window = self._parent._window
        self.location_filter = self._window.findChild(QObject, "locationDialogObj")
        self.category_filter = self._window.findChild(QObject, "categoryDialogObj")
        self.modulation_filter = self._window.findChild(QObject, "moculationDialogObj")

        self._connect()


    def _connect(self):
        # QML > Python connections
        self._window.applyFilter.connect(self.apply_filter)

        # Python > QML connections
        self.populate_filter_list.connect(self._window.populateFilterLists)


    def load_filter_lists(self):
        locations = self._parent.loaded_db.all_location
        modulations = self._parent.loaded_db.all_modulation
        categories = self._parent.loaded_db.all_category_labels

        self.populate_filter_list.emit([{
            'location': locations,
            'modulation': modulations,
            'category': categories
        }])


    @Slot(dict)
    def apply_filter(self, filter_status):
        """ Update the signal list according to the selected filters.

        Args:
            filter_status (dict): dictionary containing the active filters with all
            the details to generate a search query
        """
        filter_status = filter_status.toVariant()

        if self._parent.loaded_db is not None:
            if filter_status != {}:

                ############### TEMPORARY CODE UNTIL ORM IMPLEMENTATION (to be deleted asap) ############
                if 'category' in filter_status:
                    all_categories = self._parent.loaded_db.all_category_labels
                    category_lookup = {item['value']: item['clb_id'] for item in all_categories}

                    category_list = filter_status['category']
                    category_list = [category_lookup.get(i) for i in category_list]

                    filter_status['category'] = category_list
                ############### TEMPORARY CODE UNTIL ORM IMPLEMENTATION ############

                filter_query = generate_filter_query(filter_status)
                print(filter_query)
                self._parent.loaded_db.select_by_filter(filter_query)

                self._parent.clear_signal_page.emit()
                self._parent.populate_sig_list.emit(self._parent.loaded_db.all_signals)

                total_signals = len(self._parent.loaded_db.all_signals)
                self._parent.bottom_info_bar("FILTERS ACTIVE: {} signals found".format(total_signals), "warning")
            else:
                self._parent.load_db(self._parent.loaded_db.db_dir_name)
