import re

# Compile the regular expression once for efficiency and safety.
_LOG_ENTRY_RE = re.compile(
    r'^\[(?P<timestamp>.*?)\]\s+(?P<level>\w+):\s+(?P<message>.*)$',
    re.DOTALL
)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level, and message from a log entry.

    The expected format is:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    entry : str
        The log entry string to parse.

    Returns
    -------
    tuple | None
        A 3-tuple (timestamp, log_level, message) if parsing succeeds,
        otherwise None.
    """
    try:
        match = _LOG_ENTRY_RE.match(entry)
        if not match:
            return None
        # Retrieve named groups for clarity.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unexpected error should result in a graceful failure.
        return None