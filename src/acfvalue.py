from constants import Constants


class ACFValue:
    """Handle complex/multiple ACF values."""

    def __init__(self, value):
        """Given a string describing an acf value, build an object with the
        following attrributes:
        - is_numeric: whether the value is a number or a string;
        - numeric_value: the numeric value (if any, zero otherwise);
        - unknown: whether the value is unknown."""
        if value == Constants.UNKNOWN:
            self._value = value
            self._description = ""
            self._string = self._value
            self.is_numeric = False
            self.unknown = True
            self.numeric_value = 0.0
        else:
            self.unknown = False
            if Constants.ACF_SEPARATOR in value:
                description, acf_value = value.split(Constants.ACF_SEPARATOR)
                self._description = description
                self._value = acf_value
                self._string = f"{self._description}: {self._value}"
            else:
                self._description = ""
                self._value = value
                self._string = self._value
            try:
                self.numeric_value = float(self._value)
            except Exception:
                self.is_numeric = False
                self.numeric_value = 0.0
            else:
                self.is_numeric = True
                self._string += " ms"

    @classmethod
    def list_from_series(cls, series):
        """Parse all acf values from the database.

        Accept an iterable of ACFValues.
        Return a list of lists of ACFValues."""
        entries = []
        for entry in series:
            entries.append([
                cls(value.strip()) for value in entry.split(Constants.FIELD_SEPARATOR)
            ])
        return entries

    @staticmethod
    def concat_strings(acf_list_values):
        """Concatenate a list of ACFValues to be displayed."""
        return '\n'.join(s._string for s in acf_list_values)
