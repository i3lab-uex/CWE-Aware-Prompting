import re

# Compile the regex once for efficiency and security.
_LOG_PATTERN = re.compile(
    r'^\[(?P<timestamp>.*?)\]\s+'
    r'(?P<level>\w+):\s+'
    r'(?P<message>.*)$',
    re.DOTALL
)

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    log_line : str
        The raw log entry.

    Returns
    -------
    tuple | None
        (timestamp, log_level, message) if parsing succeeds,
        otherwise None.

    Notes
    -----
    * No exceptions are raised; errors return None.
    * The function is safe against regex injection or resource exhaustion
      because the pattern is fixed and compiled once.
    """
    if not isinstance(log_line, str):
        return None

    try:
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # In a defensive design we catch any unexpected exception and
        # simply return None, ensuring no exception propagates.
        return None