import re

# Compile the regex once for efficiency and to avoid repeated compilation overhead.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The raw log line to parse. Expected format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A tuple of (timestamp, log_level, message) if parsing succeeds,
        otherwise ``None``.
    """
    if not isinstance(entry, str):
        # Defensive: ensure we only process strings
        return None

    match = _LOG_PATTERN.match(entry)
    if not match:
        return None

    timestamp, log_level, message = match.groups()
    return timestamp, log_level, message