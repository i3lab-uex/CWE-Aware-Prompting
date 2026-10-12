import re

# Pre‑compile the regular expression for efficiency and to avoid repeated compilation.
_LOG_ENTRY_RE = re.compile(
    r"""
    ^\[
        (?P<timestamp>.+?)          # timestamp inside brackets (non‑greedy)
    \]\s+
        (?P<level>\w+)               # log level (alphanumeric)
    :\s*
        (?P<message>.*)              # message (rest of the line)
    $""",
    re.VERBOSE
)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The log entry string to parse. Expected format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A 3‑tuple (timestamp, log_level, message) if the entry matches the expected
        format. If parsing fails (e.g., wrong format or empty string), returns None.
    """
    if not isinstance(entry, str) or not entry:
        return None

    match = _LOG_ENTRY_RE.match(entry)
    if not match:
        return None

    # Extract named groups
    timestamp = match.group('timestamp')
    level = match.group('level')
    message = match.group('message')

    return timestamp, level, message