import re
from typing import Optional, Tuple

# Pre-compiled regex to avoid repeated compilation overhead.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+([A-Z]+):\s+(.*)$')

def analyze_log_data(record: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the format,
        otherwise None.

    Notes
    -----
    - The regex uses non‑greedy matching for the timestamp to avoid catastrophic backtracking.
    - No exceptions are raised; any failure simply returns None.
    """
    match = _LOG_PATTERN.match(record)
    if not match:
        return None
    timestamp, log_level, message = match.groups()
    return timestamp, log_level, message