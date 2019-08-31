"""This module contains all the filter-related classes and functions.

The only class exposed is Filters which provides the following methods:
- ok(signal_name): to check if all the filters are passed;
- reset(): to reset all the applied filters;
- refresh(): used when the theme is changed."""

from collections import namedtuple
from functools import partial
import webbrowser

from PyQt5.QtWidgets import QListWidgetItem, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QObject

from constants import (Constants,
                       Ftype,
                       Signal,)
from utilities import (uncheck_and_emit,
                       connect_events_to_func,
                       filters_limit,
                       is_undef_freq,
                       is_undef_band,
                       safe_cast,
                       show_matching_strings,
                       get_field_entries,)


class _BaseFilter(QObject):
    """Base class for all filters."""

    def __init__(self, owner):
        """Positional argument:
        owner - the object containing the filter screen."""
        super().__init__()
        self._owner = owner

    def refresh(self):
        """Refresh the screen."""
        pass


class _FreqBandMixIn:
    """Mixin class for the frequency and band filters.

    Provides some functions used in both classes."""

    @pyqtSlot()
    def _set_min_value_upper_limit(self, lower_combo_box,
                                   lower_spin_box,
                                   upper_combo_box,
                                   upper_spin_box):
        """Forbid to a lower limit to be greater than the corresponding upper one.

        Used for frequency and bandwidth screens."""
        if lower_spin_box.isEnabled():
            unit_conversion = {
                'Hz': ['kHz', 'MHz', 'GHz'],
                'kHz': ['MHz', 'GHz'],
                'MHz': ['GHz']
            }
            lower_units = lower_combo_box.currentText()
            upper_units = upper_combo_box.currentText()
            lower_value = lower_spin_box.value()
            inf_limit = (lower_value * Constants.CONVERSION_FACTORS[lower_units]) \
                // Constants.CONVERSION_FACTORS[upper_units]
            counter = 0
            while inf_limit > upper_spin_box.maximum():
                counter += 1
                inf_limit //= 1000
            if upper_spin_box.minimum() != inf_limit:
                upper_spin_box.setMinimum(inf_limit)
            if counter > 0:
                new_unit = unit_conversion[upper_units][counter - 1]
                upper_combo_box.disconnect()
                upper_combo_box.setCurrentText(new_unit)
                upper_combo_box.currentTextChanged.connect(
                    partial(
                        self._set_min_value_upper_limit,
                        lower_combo_box,
                        lower_spin_box,
                        upper_combo_box,
                        upper_spin_box
                    )
                )

    @pyqtSlot()
    def _reset_fb_filters(self, ftype):
        """Reset the Frequency or Bandwidth depending on 'ftype'.

        ftype can be either Ftype.FREQ or Ftype.BAND.
        """
        if ftype != Ftype.FREQ and ftype != Ftype.BAND:
            raise ValueError("Wrong ftype in function '_reset_fb_filters'")

        apply_remove_btn  = getattr(self._owner, 'apply_remove_'  + ftype + '_filter_btn')
        include_undef_btn = getattr(self._owner, 'include_undef_' + ftype + 's')
        activate_low      = getattr(self._owner, 'activate_low_'  + ftype + '_filter_btn')
        activate_up       = getattr(self._owner, 'activate_up_'   + ftype + '_filter_btn')
        lower_unit        = getattr(self._owner, 'lower_'         + ftype + '_filter_unit')
        upper_unit        = getattr(self._owner, 'upper_'         + ftype + '_filter_unit')
        lower_spinbox     = getattr(self._owner, 'lower_'         + ftype + '_spinbox')
        upper_spinbox     = getattr(self._owner, 'upper_'         + ftype + '_spinbox')
        lower_confidence  = getattr(self._owner, 'lower_'         + ftype + '_confidence')
        upper_confidence  = getattr(self._owner, 'lower_'         + ftype + '_confidence')

        default_val = 1 if ftype == Ftype.FREQ else 5000
        if ftype == Ftype.FREQ:
            for f in self._frequency_filters_btns:
                if f.isChecked():
                    f.setChecked(False)
        uncheck_and_emit(apply_remove_btn)
        if include_undef_btn.isChecked():
            include_undef_btn.setChecked(False)
        uncheck_and_emit(activate_low)
        uncheck_and_emit(activate_up)
        lower_unit.setCurrentText("MHz")
        upper_unit.setCurrentText("MHz")
        lower_spinbox.setValue(default_val)
        upper_spinbox.setMinimum(1)
        upper_spinbox.setValue(default_val)
        lower_confidence.setValue(0)
        upper_confidence.setValue(0)

    @pyqtSlot()
    def _set_band_filter_label(self,
                               activate_low_btn,
                               lower_spinbox,
                               lower_unit,
                               lower_confidence,
                               activate_up_btn,
                               upper_spinbox,
                               upper_unit,
                               upper_confidence,
                               range_lbl):
        """Display the actual range applied for the signal's property search.

        Used for frequency and bandwidth screens."""
        activate_low = False
        activate_high = False
        color = self._owner.inactive_color
        title = ''
        to_display = ''
        if activate_low_btn.isChecked():
            activate_low = True
            color = self._owner.active_color
            min_value = lower_spinbox.value()
            if lower_confidence.value() != 0:
                min_value -= lower_spinbox.value() * lower_confidence.value() / 100
            to_display += str(round(min_value, Constants.MAX_DIGITS)) \
                + ' ' + lower_unit.currentText()
        else:
            to_display += 'DC'
        to_display += Constants.RANGE_SEPARATOR
        if activate_up_btn.isChecked():
            max_value = upper_spinbox.value()
            activate_high = True
            color = self._owner.active_color
            if upper_confidence.value() != 0:
                max_value += upper_spinbox.value() * upper_confidence.value() / 100
            to_display += str(round(max_value, Constants.MAX_DIGITS)) + ' ' \
                + upper_unit.currentText()
        else:
            to_display += 'INF'
        if activate_low and activate_high:
            title = 'Band-pass\n\n'
        elif activate_low and not activate_high:
            title = 'Low-pass\n\n'
        elif not activate_low and activate_high:
            title = 'High-pass\n\n'
        else:
            title = "Selected range:\n\n"
            to_display = "Inactive"
        to_display = title + to_display
        range_lbl.setText(to_display)
        range_lbl.setStyleSheet(f'color: {color};')


class FreqFilter(_BaseFilter, _FreqBandMixIn):
    """Frequency filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_freq_filter_btn
        self.reset_btn = self._owner.reset_frequency_filters_btn
        self._frequency_filters_btns = (
            self._owner.elf_filter_btn,
            self._owner.slf_filter_btn,
            self._owner.ulf_filter_btn,
            self._owner.vlf_filter_btn,
            self._owner.lf_filter_btn,
            self._owner.mf_filter_btn,
            self._owner.hf_filter_btn,
            self._owner.vhf_filter_btn,
            self._owner.uhf_filter_btn,
            self._owner.shf_filter_btn,
            self._owner.ehf_filter_btn,
        )

        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                *self._frequency_filters_btns,
                self._owner.include_undef_freqs,
                self._owner.activate_low_freq_filter_btn,
                self._owner.activate_up_freq_filter_btn
            ],
            radio_1=self._owner.activate_low_freq_filter_btn,
            ruled_by_radio_1=[
                self._owner.lower_freq_spinbox,
                self._owner.lower_freq_filter_unit,
                self._owner.lower_freq_confidence
            ],
            radio_2=self._owner.activate_up_freq_filter_btn,
            ruled_by_radio_2=[
                self._owner.upper_freq_spinbox,
                self._owner.upper_freq_filter_unit,
                self._owner.upper_freq_confidence
            ]
        )

        connect_events_to_func(
            events_to_connect=[self._owner.lower_freq_spinbox.valueChanged,
                               self._owner.upper_freq_spinbox.valueChanged,
                               self._owner.lower_freq_filter_unit.currentTextChanged,
                               self._owner.upper_freq_filter_unit.currentTextChanged,
                               self._owner.activate_low_freq_filter_btn.toggled],
            fun_to_connect=self._set_min_value_upper_limit,
            fun_args=[self._owner.lower_freq_filter_unit,
                      self._owner.lower_freq_spinbox,
                      self._owner.upper_freq_filter_unit,
                      self._owner.upper_freq_spinbox]
        )

        connect_events_to_func(
            events_to_connect=[self._owner.lower_freq_spinbox.valueChanged,
                               self._owner.upper_freq_spinbox.valueChanged,
                               self._owner.lower_freq_filter_unit.currentTextChanged,
                               self._owner.upper_freq_filter_unit.currentTextChanged,
                               self._owner.activate_low_freq_filter_btn.clicked,
                               self._owner.activate_up_freq_filter_btn.clicked,
                               self._owner.lower_freq_confidence.valueChanged,
                               self._owner.upper_freq_confidence.valueChanged],
            fun_to_connect=self._set_band_filter_label,
            fun_args=[self._owner.activate_low_freq_filter_btn,
                      self._owner.lower_freq_spinbox,
                      self._owner.lower_freq_filter_unit,
                      self._owner.lower_freq_confidence,
                      self._owner.activate_up_freq_filter_btn,
                      self._owner.upper_freq_spinbox,
                      self._owner.upper_freq_filter_unit,
                      self._owner.upper_freq_confidence,
                      self._owner.freq_range_lbl]
        )

        self._owner.activate_low_freq_filter_btn.toggled.connect(
            partial(self._owner.activate_if_toggled,
                    self._owner.activate_low_freq_filter_btn,
                    self._owner.lower_freq_spinbox,
                    self._owner.lower_freq_filter_unit,
                    self._owner.lower_freq_confidence)
        )

        self._owner.activate_up_freq_filter_btn.toggled.connect(
            partial(self._owner.activate_if_toggled,
                    self._owner.activate_up_freq_filter_btn,
                    self._owner.upper_freq_spinbox,
                    self._owner.upper_freq_filter_unit,
                    self._owner.upper_freq_confidence)
        )

    @pyqtSlot()
    def reset(self):
        """Reset the filter screen."""
        self._reset_fb_filters(Ftype.FREQ)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the frequency filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        undef_freq = is_undef_freq(self._owner.db.loc[signal_name])
        if undef_freq:
            if self._owner.include_undef_freqs.isChecked():
                return True
            else:
                return False

        signal_freqs = (
            safe_cast(self._owner.db.at[signal_name, Signal.INF_FREQ], int),
            safe_cast(self._owner.db.at[signal_name, Signal.SUP_FREQ], int)
        )

        band_filter_ok = False
        any_checked = False
        for btn, band_limits in zip(self._frequency_filters_btns, Constants.BANDS):
            if btn.isChecked():
                any_checked = True
                if signal_freqs[0] < band_limits.upper and signal_freqs[1] >= band_limits.lower:
                    band_filter_ok = True
        lower_limit_ok = True
        upper_limit_ok = True
        if self._owner.activate_low_freq_filter_btn.isChecked():
            if not signal_freqs[1] >= filters_limit(self._owner.lower_freq_spinbox,
                                                    self._owner.lower_freq_filter_unit,
                                                    self._owner.lower_freq_confidence, -1):
                lower_limit_ok = False
        if self._owner.activate_up_freq_filter_btn.isChecked():
            if not signal_freqs[0] < filters_limit(self._owner.upper_freq_spinbox,
                                                   self._owner.upper_freq_filter_unit,
                                                   self._owner.upper_freq_confidence):
                upper_limit_ok = False
        if any_checked:
            return band_filter_ok and lower_limit_ok and upper_limit_ok
        else:
            return lower_limit_ok and upper_limit_ok

    def refresh(self):
        """Extend _BaseFilter.refresh."""
        super().refresh()
        self._set_band_filter_label(
            self._owner.activate_low_band_filter_btn,
            self._owner.lower_band_spinbox,
            self._owner.lower_band_filter_unit,
            self._owner.lower_band_confidence,
            self._owner.activate_up_band_filter_btn,
            self._owner.upper_band_spinbox,
            self._owner.upper_band_filter_unit,
            self._owner.upper_band_confidence,
            self._owner.band_range_lbl
        )


class BandFilter(_BaseFilter, _FreqBandMixIn):
    """Band filter class."""
    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_band_filter_btn
        self.reset_btn = self._owner.reset_band_filters_btn
        connect_events_to_func(
            events_to_connect=[self._owner.lower_band_spinbox.valueChanged,
                               self._owner.upper_band_spinbox.valueChanged,
                               self._owner.lower_band_filter_unit.currentTextChanged,
                               self._owner.upper_band_filter_unit.currentTextChanged,
                               self._owner.activate_low_band_filter_btn.toggled],
            fun_to_connect=self._set_min_value_upper_limit,
            fun_args=[self._owner.lower_band_filter_unit,
                      self._owner.lower_band_spinbox,
                      self._owner.upper_band_filter_unit,
                      self._owner.upper_band_spinbox]
        )

        connect_events_to_func(
            events_to_connect=[self._owner.lower_band_spinbox.valueChanged,
                               self._owner.upper_band_spinbox.valueChanged,
                               self._owner.lower_band_filter_unit.currentTextChanged,
                               self._owner.upper_band_filter_unit.currentTextChanged,
                               self._owner.activate_low_band_filter_btn.clicked,
                               self._owner.activate_up_band_filter_btn.clicked,
                               self._owner.lower_band_confidence.valueChanged,
                               self._owner.upper_band_confidence.valueChanged],
            fun_to_connect=self._set_band_filter_label,
            fun_args=[self._owner.activate_low_band_filter_btn,
                      self._owner.lower_band_spinbox,
                      self._owner.lower_band_filter_unit,
                      self._owner.lower_band_confidence,
                      self._owner.activate_up_band_filter_btn,
                      self._owner.upper_band_spinbox,
                      self._owner.upper_band_filter_unit,
                      self._owner.upper_band_confidence,
                      self._owner.band_range_lbl]
        )

        self._owner.activate_low_band_filter_btn.toggled.connect(
            partial(self._owner.activate_if_toggled,
                    self._owner.activate_low_band_filter_btn,
                    self._owner.lower_band_spinbox,
                    self._owner.lower_band_filter_unit,
                    self._owner.lower_band_confidence)
        )

        self._owner.activate_up_band_filter_btn.toggled.connect(
            partial(self._owner.activate_if_toggled,
                    self._owner.activate_up_band_filter_btn,
                    self._owner.upper_band_spinbox,
                    self._owner.upper_band_filter_unit,
                    self._owner.upper_band_confidence)
        )

        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                self._owner.include_undef_bands,
                self._owner.activate_low_band_filter_btn,
                self._owner.activate_up_band_filter_btn
            ],
            radio_1=self._owner.activate_low_band_filter_btn,
            ruled_by_radio_1=[
                self._owner.lower_band_spinbox,
                self._owner.lower_band_filter_unit,
                self._owner.lower_band_confidence
            ],
            radio_2=self._owner.activate_up_band_filter_btn,
            ruled_by_radio_2=[
                self._owner.upper_band_spinbox,
                self._owner.upper_band_filter_unit,
                self._owner.upper_band_confidence
            ]
        )

    @pyqtSlot()
    def reset(self):
        """Reset the filter screen."""
        self._reset_fb_filters(Ftype.BAND)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the band filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        undef_band = is_undef_band(self._owner.db.loc[signal_name])
        if undef_band:
            if self._owner.include_undef_bands.isChecked():
                return True
            else:
                return False

        signal_bands = (
            safe_cast(self._owner.db.at[signal_name, Signal.INF_BAND], int),
            safe_cast(self._owner.db.at[signal_name, Signal.SUP_BAND], int)
        )

        lower_limit_ok = True
        upper_limit_ok = True
        if self._owner.activate_low_band_filter_btn.isChecked():
            if not signal_bands[1] >= filters_limit(self._owner.lower_band_spinbox,
                                                    self._owner.lower_band_filter_unit,
                                                    self._owner.lower_band_confidence, -1):
                lower_limit_ok = False
        if self._owner.activate_up_band_filter_btn.isChecked():
            if not signal_bands[0] < filters_limit(self._owner.upper_band_spinbox,
                                                   self._owner.upper_band_filter_unit,
                                                   self._owner.upper_band_confidence):
                upper_limit_ok = False
        return lower_limit_ok and upper_limit_ok

    def refresh(self):
        """Extend _BaseFilter.refresh."""
        super().refresh()
        self._set_band_filter_label(
            self._owner.activate_low_freq_filter_btn,
            self._owner.lower_freq_spinbox,
            self._owner.lower_freq_filter_unit,
            self._owner.lower_freq_confidence,
            self._owner.activate_up_freq_filter_btn,
            self._owner.upper_freq_spinbox,
            self._owner.upper_freq_filter_unit,
            self._owner.upper_freq_confidence,
            self._owner.freq_range_lbl
        )


class CatFilter(_BaseFilter):
    """Category filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_cat_filter_btn
        self.reset_btn = self._owner.reset_cat_filters_btn
        # Order matters!
        self._cat_filter_btns = [
            self._owner.military_btn,
            self._owner.radar_btn,
            self._owner.active_btn,
            self._owner.inactive_btn,
            self._owner.ham_btn,
            self._owner.commercial_btn,
            self._owner.aviation_btn,
            self._owner.marine_btn,
            self._owner.analogue_btn,
            self._owner.digital_btn,
            self._owner.trunked_btn,
            self._owner.utility_btn,
            self._owner.sat_btn,
            self._owner.navigation_btn,
            self._owner.interfering_btn,
            self._owner.number_stations_btn,
            self._owner.time_signal_btn
        ]

        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                *self._cat_filter_btns,
                self._owner.cat_at_least_one,
                self._owner.cat_all
            ]
        )

    @pyqtSlot()
    def reset(self):
        """Reset the category filter screen."""
        uncheck_and_emit(self.apply_remove_btn)
        for f in self._cat_filter_btns:
            if f.isChecked():
                f.setChecked(False)
        self._owner.cat_at_least_one.setChecked(True)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the category filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        cat_code = self._owner.db.at[signal_name, Signal.CATEGORY_CODE]
        cat_checked = 0
        positive_cases = 0
        for index, cat in enumerate(self._cat_filter_btns):
            if cat.isChecked():
                cat_checked += 1
                if cat_code[index] == '1':
                    positive_cases += 1
        if self._owner.cat_at_least_one.isChecked():
            return positive_cases > 0
        else:
            return cat_checked == positive_cases and cat_checked > 0


class ModeFilter(_BaseFilter):
    """Mode filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_mode_filter_btn
        self.reset_btn = self._owner.reset_mode_filters_btn
        self._set_mode_tree_widget()
        self._owner.mode_tree_widget.itemSelectionChanged.connect(
            self._manage_mode_selections
        )
        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                self._owner.mode_tree_widget,
                self._owner.include_unknown_modes_btn
            ]
        )

    def _manage_mode_selections(self):
        """Rules the selection of childs items of the 'Mode' QTreeWidget.

        If a parent is selected all its children will be selected as well.
        """
        selected_items = self._owner.mode_tree_widget.selectedItems()
        parents = Constants.MODES.keys()
        for parent in parents:
            for item in selected_items:
                if parent == item.text(0):
                    for i in range(len(Constants.MODES[parent])):
                        item.child(i).setSelected(True)

    def _set_mode_tree_widget(self):
        """Construct the QTreeWidget for the 'Mode' screen."""
        for parent, children in Constants.MODES.items():
            iparent = QTreeWidgetItem([parent])
            self._owner.mode_tree_widget.addTopLevelItem(iparent)
            for child in children:
                ichild = QTreeWidgetItem([child])
                iparent.addChild(ichild)
        self._owner.mode_tree_widget.expandAll()

    @pyqtSlot()
    def reset(self):
        """Reset the mode filter screen."""
        uncheck_and_emit(self.apply_remove_btn)
        parents = Constants.MODES.keys()
        selected_children = []
        for item in self._owner.mode_tree_widget.selectedItems():
            if item.text(0) in parents:
                item.setSelected(False)
            else:
                selected_children.append(item)
        for children in selected_children:
            children.setSelected(False)
        if self._owner.include_unknown_modes_btn.isChecked():
            self._owner.include_unknown_modes_btn.setChecked(False)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the mode filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        signal_mode = self._owner.db.at[signal_name, Signal.MODE]
        if signal_mode == Constants.UNKNOWN:
            if self._owner.include_unknown_modes_btn.isChecked():
                return True
            else:
                return False
        selected_items = [item for item in self._owner.mode_tree_widget.selectedItems()]
        selected_items_text = [i.text(0) for i in selected_items]
        parents = [
            item for item in selected_items_text
            if item in Constants.MODES.keys()
        ]
        ok = []
        for item in selected_items:
            if item.text(0) in parents:
                ok.append(item.text(0) in signal_mode)
            elif not item.parent().isSelected():
                ok.append(item.text(0) == signal_mode)
        return any(ok)


class ModulationFilter(_BaseFilter):
    """Modulation filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_modulation_filter_btn
        self.reset_btn = self._owner.reset_modulation_filters_btn
        self._owner.search_bar_modulation.textEdited.connect(self._show_matching_modulations)
        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                self._owner.search_bar_modulation,
                self._owner.modulation_list
            ]
        )
        self._owner.modulation_list.itemClicked.connect(self._remove_if_unselected_modulation)

    @pyqtSlot(QListWidgetItem)
    def _remove_if_unselected_modulation(self, item):
        """If an item is unselected from the modulations list, hide the item."""
        if not item.isSelected():
            self._show_matching_modulations(self.search_bar_modulation.text())

    @pyqtSlot(str)
    def _show_matching_modulations(self, text):
        """Show the modulations which matches 'text'.

        The match criterion is defined in 'show_matching_strings'."""
        show_matching_strings(self._owner.modulation_list, text)

    @pyqtSlot()
    def reset(self):
        """Reset the modulation filter screen."""
        uncheck_and_emit(self.apply_remove_btn)
        self._owner.search_bar_modulation.setText('')
        show_matching_strings(
            self._owner.modulation_list,
            self._owner.search_bar_modulation.text()
        )
        for i in range(self._owner.modulation_list.count()):
            if self._owner.modulation_list.item(i).isSelected():
                self._owner.modulation_list.item(i).setSelected(False)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the modulation filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        signal_modulation = get_field_entries(
            self._owner.db.at[signal_name, Signal.MODULATION]
        )
        for item in self._owner.modulation_list.selectedItems():
            if item.text() in signal_modulation:
                return True
        return False


class LocFilter(_BaseFilter):
    """Location filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_location_filter_btn
        self.reset_btn = self._owner.reset_location_filters_btn
        self._owner.search_bar_location.textEdited.connect(
            self._show_matching_locations
        )
        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                self._owner.search_bar_location,
                self._owner.locations_list
            ]
        )
        self._owner.locations_list.itemClicked.connect(self._remove_if_unselected_location)

    @pyqtSlot(str)
    def _show_matching_locations(self, text):
        """Show the locations which matches 'text'.

        The match criterion is defined in 'show_matching_strings'."""
        show_matching_strings(self._owner.locations_list, text)

    @pyqtSlot(QListWidgetItem)
    def _remove_if_unselected_location(self, item):
        """If an item is unselected from the locations list, hide the item."""
        if not item.isSelected():
            self._show_matching_locations(self._owner.search_bar_location.text())

    @pyqtSlot()
    def reset(self):
        """Reset the location filter screen."""
        uncheck_and_emit(self.apply_remove_btn)
        self._owner.search_bar_location.setText('')
        show_matching_strings(
            self._owner.locations_list,
            self._owner.search_bar_location.text()
        )
        for i in range(self._owner.locations_list.count()):
            if self._owner.locations_list.item(i).isSelected():
                self._owner.locations_list.item(i).setSelected(False)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the location filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        signal_locations = get_field_entries(
            self._owner.db.at[signal_name, Signal.LOCATION]
        )
        for item in self._owner.locations_list.selectedItems():
            if item.text() in signal_locations:
                return True
        return False


class ACFFilter(_BaseFilter):
    """Autocorrelation function filter class."""

    def __init__(self, owner):
        super().__init__(owner)
        self.apply_remove_btn = self._owner.apply_remove_acf_filter_btn
        self.reset_btn = self._owner.reset_acf_filters_btn
        self.apply_remove_btn.set_texts(Constants.APPLY, Constants.REMOVE)
        self.apply_remove_btn.set_slave_filters(
            simple_ones=[
                self._owner.include_undef_acf,
                self._owner.acf_spinbox,
                self._owner.acf_confidence
            ]
        )
        self._owner.acf_info_btn.clicked.connect(lambda: webbrowser.open(Constants.ACF_DOCS))

        connect_events_to_func(
            events_to_connect=[self._owner.acf_spinbox.valueChanged,
                               self._owner.acf_confidence.valueChanged],
            fun_to_connect=self._set_acf_interval_label,
            fun_args=None
        )

    @pyqtSlot()
    def _set_acf_interval_label(self):
        """Display the actual acf interval for the search."""
        tolerance = self._owner.acf_spinbox.value() * self._owner.acf_confidence.value() / 100
        if tolerance > 0:
            val = round(self._owner.acf_spinbox.value() - tolerance, Constants.MAX_DIGITS)
            to_display = f"Selected range:\n\n{val}" + Constants.RANGE_SEPARATOR \
                + f"{round(self._owner.acf_spinbox.value() + tolerance, Constants.MAX_DIGITS)} ms"
        else:
            to_display = f"Selected value:\n\n{self._owner.acf_spinbox.value()} ms"
        self._owner.acf_range_lbl.setText(to_display)
        self._owner.acf_range_lbl.setStyleSheet(f"color: {self._owner.active_color}")

    @pyqtSlot()
    def reset(self):
        """Reset the acf filter screen."""
        uncheck_and_emit(self.apply_remove_btn)
        if self._owner.include_undef_acf.isChecked():
            self._owner.include_undef_acf.setChecked(False)
        self._owner.acf_spinbox.setValue(50)
        self._owner.acf_confidence.setValue(0)

    def _ok(self, signal_name):
        """Evalaute if the signal matches the acf filters."""
        if not self.apply_remove_btn.isChecked():
            return True
        signal_acf = self._owner.db.at[signal_name, Signal.ACF]
        if signal_acf == Constants.UNKNOWN:
            if self._owner.include_undef_acf.isChecked():
                return True
            else:
                return False
        else:
            signal_acf = safe_cast(signal_acf.rstrip("ms"), float)
            tolerance = self._owner.acf_spinbox.value() * self._owner.acf_confidence.value() / 100
            upper_limit = self._owner.acf_spinbox.value() + tolerance
            lower_limit = self._owner.acf_spinbox.value() - tolerance
            if signal_acf <= upper_limit and signal_acf >= lower_limit:
                return True
            else:
                return False

    def refresh(self):
        """Extend _BaseFilter.refresh."""
        super().refresh()
        self._set_acf_interval_label()


class Filters(QObject):
    """Global filter class.

    Provides the information about all the filters. Its only public attribute
    is filters, which is a namedtuple containing instances of all the filters.
    The only exposed methods are reset(), ok(signal_name) and refresh().
    The class also connects the apply and reset buttons to the relevant functions."""

    _FiltersTuple = namedtuple(
        "_FiltersTuple",
        [
            "freq_filter",
            "band_filter",
            "cat_filter",
            "mode_filter",
            "modulation_filter",
            "location_filter",
            "acf_filter",
        ]
    )

    def __init__(self, owner):
        super().__init__()
        self.filters = self._FiltersTuple(
            FreqFilter(owner),
            BandFilter(owner),
            CatFilter(owner),
            ModeFilter(owner),
            ModulationFilter(owner),
            LocFilter(owner),
            ACFFilter(owner),
        )
        self._owner = owner
        self._owner.reset_filters_btn.clicked.connect(self.reset)

        # Connect Apply and Reset buttons clicks to functions.
        for f in self.filters:
            f.apply_remove_btn.clicked.connect(self._display_signals)
            f.reset_btn.clicked.connect(f.reset)

    @pyqtSlot()
    def _display_signals(self):
        self._owner.display_signals()

    @pyqtSlot()
    def reset(self):
        """Reset all the filters."""
        for f in self.filters:
            f.reset()

    def ok(self, signal_name):
        """Check whether all the filters are passed."""
        return all(f._ok(signal_name) for f in self.filters)

    def refresh(self):
        """Refresh the relevant widgets when changing theme."""
        for f in self.filters:
            f.refresh()
