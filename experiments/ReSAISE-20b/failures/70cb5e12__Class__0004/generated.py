import re

# Compile the pattern once for efficiency and to avoid repeated recompilation.
_LOG_PATTERN = re.compile(r'^\[(.+?)\]\s+(\w+):\s+(.*)$')

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the
        expected format; otherwise None.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract the three captured groups.
        timestamp, log_level, message = match.groups()
        return timestamp, log_level, message
    except Exception:
        # Swallow any unexpected error to satisfy the "no exceptions" requirement.
        return None