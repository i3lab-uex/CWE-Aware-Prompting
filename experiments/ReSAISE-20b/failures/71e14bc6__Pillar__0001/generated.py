import re

# Regular expression to match a log entry of the form:
# [TIMESTAMP] LOG_LEVEL: MESSAGE
_LOG_ENTRY_RE = re.compile(r"""
    ^\[
        (?P<timestamp>[^]]+)
    \]\s+
    (?P<level>[A-Z]+):\s*
    (?P<message>.*)
""", re.VERBOSE)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a single log entry.

    Parameters
    ----------
    entry : str
        A string representing the individual log entry. Expected format:
        '[TIMESTAMP] LOG_LEVEL: MESSAGE'

    Returns
    -------
    tuple | None
        A 3‑tuple (timestamp, log_level, message) if the entry matches the
        expected format; otherwise None.
    """
    try:
        match = _LOG_ENTRY_RE.fullmatch(entry.strip())
        if not match:
            return None
        return (
            match.group('timestamp'),
            match.group('level'),
            match.group('message')
        )
    except Exception:
        # Ensure no exception propagates to the caller
        return None