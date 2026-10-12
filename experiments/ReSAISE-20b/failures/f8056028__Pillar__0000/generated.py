import re
from typing import Optional, Tuple

# Pre‑compiled regular expression for performance and safety.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s*(?P<message>.*)$')

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters
    ----------
    log_line : str
        The raw log entry to parse.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if parsing succeeds;
        otherwise None.

    Notes
    -----
    The function is intentionally defensive: it never raises an exception,
    even if the input is malformed or contains unexpected characters.
    """
    try:
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unforeseen error results in a graceful failure.
        return None