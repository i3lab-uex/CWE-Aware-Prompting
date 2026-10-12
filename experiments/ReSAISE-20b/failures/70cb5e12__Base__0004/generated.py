import re
from typing import Optional, Tuple

# Compile a safe, anchored regular expression that captures the three parts
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def analyze_log_data(record: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches.
        Returns None for malformed entries or on any internal error.

    Notes
    -----
    - The function is defensive: it catches all exceptions and returns None.
    - The regular expression is anchored to the start (^) and end ($) of the string
      and uses non-greedy matching for the timestamp to avoid catastrophic backtracking.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        timestamp, log_level, message = match.groups()
        return timestamp, log_level, message
    except Exception:
        # In a security‑critical environment we would log the exception details,
        # but for this function we simply return None to avoid leaking information.
        return None