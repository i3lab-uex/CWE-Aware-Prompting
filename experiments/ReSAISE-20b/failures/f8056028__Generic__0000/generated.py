import re
from typing import Optional, Tuple

# Compile the pattern once for efficiency and security
_LOG_PATTERN = re.compile(
    r'^\[(?P<ts>[^]]+)\]\s*(?P<level>\w+):\s*(?P<msg>.*)$'
)

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The raw log entry string.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None.
    """
    # Quick type and emptiness check to avoid unnecessary work
    if not isinstance(log_line, str) or not log_line:
        return None

    try:
        match = _LOG_PATTERN.match(log_line)
    except re.error:
        # In the unlikely event that the regex is malformed,
        # we fail gracefully instead of propagating an exception.
        return None

    if not match:
        return None

    # Extract named groups; they are guaranteed to exist due to the pattern
    ts = match.group('ts')
    level = match.group('level')
    msg = match.group('msg')

    return ts, level, msg