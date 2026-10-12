import re

# Compile the regex once for efficiency and safety.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s*(?P<message>.+)$')

def analyze_log_data(record: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches the expected format.
        Returns None for malformed entries or if any error occurs during parsing.

    Notes
    -----
    The function is intentionally forgiving: it never raises an exception.
    It simply returns None if the input does not conform to the pattern or if any unexpected
    error occurs (e.g., non-string input). This ensures robustness in environments where
    log data may be noisy or incomplete.
    """
    try:
        if not isinstance(record, str):
            return None
        match = _LOG_PATTERN.fullmatch(record.strip())
        if not match:
            return None
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unexpected error results in a graceful None return.
        return None