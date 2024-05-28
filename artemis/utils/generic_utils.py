from artemis.utils.constants import Query


def format_frequency(freq_hz):
    """ Return frequency in a human-readable format

    Args:
        freq_hz (int): frequency in Hz
    """
    scale = _change_unit_freq(freq_hz)
    formatted_freq = f'{freq_hz / scale[0]} {scale[1]}'
    return formatted_freq


def _change_unit_freq(freq_hz):
    """ Return a scale factor and unit based on the number of digits in the frequency

    Args:
        freq_hz (int): frequency in Hz
    """
    digits = len(str(freq_hz))

    if digits < 4:
        return 1, 'Hz'
    elif digits < 7:
        return 10**3, 'kHz'
    elif digits < 10:
        return 10**6, 'MHz'
    else:
        return 10**9, 'GHz'


def generate_filter_query(filer_status):
    """ Returns the sql query according to the selected filter parameters 

    Args:
        filer_status (dic): dictionary containing a summary of the active
        filtering options with the related parametes.
    """
    query = []

    for key, val in filer_status.items():

        if key == 'frequency':
            query.append(Query.FILTER_FREQ.format(
                val['upper_band'],
                val['lower_band']
            ))

        elif key == 'bandwidth':
            query.append(Query.FILTER_BAND.format(
                val['upper_band'],
                val['lower_band']
            ))

        elif key == 'acf':
            query.append(Query.FILTER_ACF.format(
                val['upper_band'],
                val['lower_band']
            ))

        elif key == 'modulation':
            query.append(Query.FILTER_MODULATION.format(
                ', '.join(f"'{mod}'" for mod in val)
            ))

        elif key == 'location':
            query.append(Query.FILTER_LOCATION.format(
                ', '.join(f"'{loc}'" for loc in val)
            ))

        elif key == 'category':
            query.append(Query.FILTER_CATEGORY.format(
                ', '.join(f"{cat}" for cat in val)
            ))

    return ' INTERSECT '.join(query)
