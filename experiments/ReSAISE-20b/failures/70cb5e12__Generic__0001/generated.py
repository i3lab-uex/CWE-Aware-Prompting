import re

# Compile the regex once for efficiency and safety.
_LOG_PATTERN = re.compile(r"""
    \[            # Opening bracket
    (?P<ts>[^]]+) # Anything except closing bracket as timestamp
    \]            # Closing bracket
    \s+           # One or more whitespace characters
    (?P<level>\w+)# Log level (alphanumeric word)
    :             # Colon separator
    \s*           # Optional whitespace after colon
    (?P<msg>.*)   # Rest of the line as message (can be empty)
    """, re.VERBOSE)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple or None
        (timestamp, log_level, message) if the entry matches the format,
        otherwise None.

    Notes
    -----
    The function never raises an exception.  It simply returns None on any
    parsing failure or if the input is not a string.
    """
    # Guard against non-string inputs
    if not isinstance(record, str):
        return None

    try:
        match = _LOG_PATTERN.fullmatch(record)
        if not match:
            return None
        ts = match.group('ts')
        level = match.group('level')
        msg = match.group('msg')
        return ts, level, msg
    except Exception:
        # Catch any unforeseen errors and return None instead of propagating
        return None