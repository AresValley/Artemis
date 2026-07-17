from datetime import datetime


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


def parse_date(date_str):
    """ Parses a date string in "%Y-%m-%d %H:%M:%S.%f" format and returns
    the date in "YYYY-MM-DD" format. If parsing fails, returns the original string.

    Args:
        date_str (str): The date string to parse.
    """
    try:
        form_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        return str(form_date.date())
    except ValueError:
        return date_str
