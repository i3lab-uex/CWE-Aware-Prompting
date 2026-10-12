import re
from typing import Optional, Tuple

# Compile the regex once to avoid repeated compilation overhead.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s*(?P<message>.*)$')

def analyze_log_entry(entry: str) -> Optional[Tuple[str, str, str]]:
    """
    Extract the timestamp, log level, and message from a log entry.

    Parameters
    ----------
    entry : str
        The log entry string in the format '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple (timestamp, log_level, message) if the entry matches the expected
        format; otherwise None.

    Notes
    -----
    No exceptions are raised. The function safely handles malformed input by returning
    None.  The compiled regular expression is stored in a module-level constant to
    prevent unnecessary re-compilation on each call, ensuring efficient resource usage.
    """
    match = _LOG_PATTERN.match(entry)
    if not match:
        return None
    return (
        match.group('timestamp'),
        match.group('level'),
        match.group('message')
    )