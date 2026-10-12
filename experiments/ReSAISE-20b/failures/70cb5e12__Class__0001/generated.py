import re
from typing import Optional, Tuple

# Pre‑compile the pattern to avoid recompilation on every call.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>[A-Z]+):\s*(?P<message>.*)$')

def analyze_log_data(record: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The raw log entry string.

    Returns
    -------
    tuple[str, str, str] | None
        A 3‑tuple containing (timestamp, log_level, message) if the entry matches the
        expected format.  Otherwise returns None.

    Notes
    -----
    The function never raises an exception; malformed input simply yields None.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract groups in the required order.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unexpected error (e.g., type issues) is swallowed to meet the spec.
        return None