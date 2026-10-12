import re

# Compile the regular expression once for efficiency and security.
_LOG_ENTRY_PATTERN = re.compile(
    r'^\[(?P<timestamp>[^\]]+)\]\s+(?P<level>\w+):\s+(?P<message>.+)$',
    re.UNICODE
)

def analyze_log_entry(entry: str):
    """
    Extracts the timestamp, log level, and message from a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    entry : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None. No exceptions are raised.
    """
    if not isinstance(entry, str):
        return None

    match = _LOG_ENTRY_PATTERN.fullmatch(entry.strip())
    if not match:
        return None

    # Safely extract the named groups
    timestamp = match.group('timestamp')
    log_level = match.group('level')
    message = match.group('message')

    return timestamp, log_level, message