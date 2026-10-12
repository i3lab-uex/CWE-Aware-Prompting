import re

# Regular expression that matches the log format:
#   [TIMESTAMP] LOG_LEVEL: MESSAGE
LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)   # anything up to the closing bracket
    \]\s+
        (?P<log_level>\w+):\s+
        (?P<message>.*)       # rest of the line
    $""",
    re.VERBOSE,
)

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
        (timestamp, log_level, message) if the record matches the expected format,
        otherwise None.
    """
    # Defensive: ensure input is a string
    if not isinstance(record, str):
        return None

    match = LOG_PATTERN.fullmatch(record.strip())
    if not match:
        return None

    # Extract groups safely
    timestamp = match.group('timestamp')
    log_level = match.group('log_level')
    message = match.group('message')

    return timestamp, log_level, message