import re
from typing import Optional, Tuple

# Pre‑compile the regular expression to avoid recompilation on every call.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s+(?P<message>.+)$')

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log line of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The raw log entry string.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if the line matches
        the expected format; otherwise None.

    Notes
    -----
    - The function never raises an exception.
    - Uses a pre‑compiled regex with named groups for clarity and efficiency.
    """
    try:
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        # Extract named groups to avoid index errors and improve readability.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # In case of unexpected errors (e.g., invalid input types), return None.
        return None