import re

# Compile a safe, non‑greedy regular expression for log entry parsing.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def extract_log_data(log_line: str):
    """
    Parse a log line of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The raw log entry string.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the line matches,
        otherwise None.

    Notes
    -----
    * The function never raises an exception; malformed input simply results in None.
    * The regex is deliberately simple and non‑greedy to avoid catastrophic backtracking
      (CWE-1333).
    """
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    timestamp, log_level, message = match.groups()
    return timestamp, log_level, message