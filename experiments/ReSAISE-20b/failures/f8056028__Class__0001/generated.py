import re
from typing import Optional, Tuple

# Compile the regex once at module load time for efficiency.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+([A-Z]+):\s+(.*)$')

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    log_line : str
        The log entry string to be parsed.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if parsing is
        successful; otherwise None.

    Notes
    -----
    - The function never raises an exception; any malformed input simply
      results in a return value of None.
    - The regular expression is intentionally simple and non-backtracking
      to avoid worst‑case performance issues (CWE‑407).
    """
    try:
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        timestamp, log_level, message = match.groups()
        return timestamp, log_level, message
    except Exception:
        # Defensive catch: any unexpected error results in None rather than an exception.
        return None