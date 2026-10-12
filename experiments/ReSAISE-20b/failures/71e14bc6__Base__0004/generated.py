import re

# Compile the regex once for efficiency and to avoid excessive backtracking.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level, and message from a log entry.

    Parameters
    ----------
    entry : str
        A string representing the individual log entry in the format:
        '[TIMESTAMP] LOG_LEVEL: MESSAGE'

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the format,
        otherwise None.

    Notes
    -----
    - The function is defensive: it never raises an exception.
    - The regular expression uses non-greedy matching for the timestamp
      and a simple word pattern for the log level to keep complexity linear.
    """
    if not isinstance(entry, str):
        return None

    match = _LOG_PATTERN.match(entry)
    if not match:
        return None

    timestamp, log_level, message = match.groups()
    return timestamp, log_level, message