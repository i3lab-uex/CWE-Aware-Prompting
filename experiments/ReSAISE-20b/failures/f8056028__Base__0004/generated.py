import re
from typing import Optional, Tuple

# Pre-compile the regular expression for efficiency and reuse.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Extracts timestamp, log level and message from a log entry.

    Expected format: '[TIMESTAMP] LOG_LEVEL: MESSAGE'

    Parameters
    ----------
    log_line : str
        The raw log entry string.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple (timestamp, log_level, message) if parsing succeeds;
        otherwise None.

    Notes
    -----
    * The function never raises exceptions; it returns ``None`` on any error.
    * The regular expression is anchored and uses a non‑greedy match for the
      timestamp to avoid catastrophic backtracking (CWE‑1333).
    """
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    timestamp, log_level, message = match.groups()
    # Basic sanity checks
    if not (timestamp and log_level and message):
        return None

    return timestamp, log_level, message