import re

# Pre‑compiled regular expression for performance and safety
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s+(?P<message>.*)$')

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        A single log line in the format: "[TIMESTAMP] LOG_LEVEL: MESSAGE"

    Returns
    -------
    tuple[str, str, str] | None
        A 3‑tuple (timestamp, log_level, message) if the entry matches the expected
        format; otherwise ``None``. No exceptions are raised.
    """
    if not isinstance(entry, str):
        # If entry is not a string, we cannot parse it.
        return None

    match = _LOG_PATTERN.fullmatch(entry.strip())
    if not match:
        return None

    # Extract named groups; they are guaranteed to exist due to the regex.
    timestamp = match.group('timestamp')
    log_level = match.group('level')
    message = match.group('message')

    return timestamp, log_level, message