import re

# Pre‑compile the regex for efficiency and to avoid repeated compilation.
_LOG_ENTRY_RE = re.compile(r'^\[(?P<timestamp>.*?)\]\s+(?P<level>\w+):\s+(?P<message>.*)$')

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    The expected format is:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    entry : str
        A single log line.

    Returns
    -------
    tuple | None
        (timestamp, log_level, message) if the entry matches the format,
        otherwise ``None``.
    """
    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _LOG_ENTRY_RE.fullmatch(entry)
    if not match:
        return None

    # Extract named groups; they are already strings.
    timestamp = match.group('timestamp')
    log_level = match.group('level')
    message = match.group('message')

    return timestamp, log_level, message