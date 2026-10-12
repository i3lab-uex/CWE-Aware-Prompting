import re

# Pre‑compiled regular expression for performance and security
_LOG_ENTRY_RE = re.compile(
    r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s*(?P<message>.*)$',
    re.ASCII
)

def analyze_log_entry(entry: str):
    """
    Extract timestamp, log level and message from a log entry.

    The expected format is:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    entry : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format.  Returns None when parsing fails.
    """
    try:
        match = _LOG_ENTRY_RE.match(entry)
        if not match:
            return None
        # Retrieve named groups; they are guaranteed to exist because the regex
        # matched successfully.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unexpected error (e.g., None passed in) results in a graceful
        # failure rather than an exception.
        return None