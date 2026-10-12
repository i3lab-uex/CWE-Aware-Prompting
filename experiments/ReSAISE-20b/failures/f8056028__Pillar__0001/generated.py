import re

# Pre-compiled regular expression for efficiency and safety.
_LOG_PATTERN = re.compile(
    r'^\[(?P<timestamp>.*?)\]\s+(?P<level>\w+):\s+(?P<message>.+)$'
)

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The raw log line to be parsed.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the line matches
        the expected format; otherwise None.
    """
    # Guard against non-string inputs to avoid type errors.
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    # Extract named groups for clarity.
    timestamp = match.group('timestamp')
    level = match.group('level')
    message = match.group('message')

    # Basic validation: ensure none of the components are empty.
    if not (timestamp and level and message):
        return None

    return timestamp, level, message