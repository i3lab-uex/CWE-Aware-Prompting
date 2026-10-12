import re

# Compile the regex once to avoid repeated compilation overhead.
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
        A tuple containing (timestamp, log_level, message) if the line matches the
        expected format; otherwise None. No exception is raised for malformed input.
    """
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    # The regex guarantees three capturing groups.
    timestamp, log_level, message = match.group(1), match.group(2), match.group(3)
    return timestamp, log_level, message