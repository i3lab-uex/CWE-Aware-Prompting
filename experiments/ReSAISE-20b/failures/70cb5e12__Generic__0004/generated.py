import re

# Pre‑compile the regular expression for efficiency and safety.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>.+?)\]\s+(?P<level>\w+):\s+(?P<message>.+)$')

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches the
        expected format; otherwise, None.

    Notes
    -----
    - The function never raises an exception.
    - Uses a pre‑compiled regular expression to avoid repeated compilation overhead.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract named groups for clarity and safety.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # In the unlikely event of an unexpected error (e.g., re module failure),
        # return None to satisfy the "no exceptions" contract.
        return None