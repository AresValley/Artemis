from PySide6.QtCore import QObject, Slot, Signal

from peewee import ModelSelect

from artemis.model import (
    database, Signals, Category, CategoryLabel, Frequency, Bandwidth, 
    Modulation, Location, Acf
)


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
        locations = self._parent.loaded_db.all_locations
        modulations = self._parent.loaded_db.all_modulations
        categories = self._parent.loaded_db.all_category_labels
        since_versions = self._parent.loaded_db.all_since_versions

        self.populate_filter_list.emit([{
            'location': locations,
            'modulation': modulations,
            'category': categories,
            'since_version': since_versions
        }])


    @Slot(dict)
    def apply_filter(self, filter_status: dict):
        """ Update the signal list according to the selected filters.

        Args:
            filter_status (dict): dictionary containing the active filters with all
            the details to generate a search query
        """
        filter_status = filter_status.toVariant()

        if self._parent.loaded_db is not None:
            # If filter_status is empty then reload all signals back
            if not filter_status:
                self._parent.loaded_db._select_all_signals()
                self._parent.clear_signal_page.emit()
                self._parent.populate_sig_list.emit(self._parent.loaded_db.all_signals)
                self._parent.bottom_info_bar(
                    f"{self._parent.loaded_db.name} v{self._parent.loaded_db.version} | {self._parent.loaded_db.count_signals} signals",
                    "info"
                )
                return

            try:
                filtered_signals = self._get_filtered_signals_query(filter_status)

                self._parent.loaded_db.all_signals = filtered_signals

                self._parent.clear_signal_page.emit()
                self._parent.populate_sig_list.emit(filtered_signals)

                total_signals = len(filtered_signals)
                self._parent.bottom_info_bar(
                    f"{self._parent.loaded_db.name} v{self._parent.loaded_db.version} | {total_signals} ({self._parent.loaded_db.count_signals}) signals | FILTERS ACTIVE",
                    "warning"
                )

            except Exception as e:
                self._parent.bottom_info_bar(f"Error applying filters: {e}", "danger")


    def _get_filtered_signals_query(self, filter_status: dict) -> ModelSelect:
        """ Generete query using the applied filters summarized in the dictionary
        """
        with database:
            query = (Signals.select(Signals.sig_id, Signals.name, Signals.description))

            conditions = []
            joined_models = set()

            def apply_join(model):
                nonlocal query
                # Check if the model has not been joined yet to avoid redundant joins
                if model not in joined_models:
                    query = query.switch(Signals).join(model)
                    # Mark the model as joined by adding it to the set
                    joined_models.add(model)

            # Iterate through each filter key and value provided in the dictionary
            for key, val in filter_status.items():
                if not val:
                    continue

                if key == 'frequency':
                    apply_join(Frequency)
                    conditions.append(Frequency.value.between(val['lower_band'], val['upper_band']))

                elif key == 'bandwidth':
                    apply_join(Bandwidth)
                    conditions.append(Bandwidth.value.between(val['lower_band'], val['upper_band']))

                elif key == 'acf':
                    apply_join(Acf)
                    conditions.append(Acf.value.between(val['lower_band'], val['upper_band']))

                elif key == 'modulation':
                    apply_join(Modulation)
                    conditions.append(Modulation.value.in_(val))

                elif key == 'location':
                    apply_join(Location)
                    conditions.append(Location.value.in_(val))

                elif key == 'since_version':
                    conditions.append(Signals.since_version.in_(val))

                elif key == 'category':
                    if Category not in joined_models:
                        query = query.switch(Signals).join(Category).join(CategoryLabel)
                        joined_models.add(Category)
                    conditions.append(CategoryLabel.value.in_(val))

            if conditions:
                # Unpack and apply all collected conditions to the query using an AND logic
                query = query.where(*conditions)

            query = query.distinct().dicts()

            return list(query)
