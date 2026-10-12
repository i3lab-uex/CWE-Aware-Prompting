import re

# Compile the regex pattern once to avoid recompilation on every call.
# The pattern captures:
#   1. Timestamp inside square brackets
#   2. Log level consisting of uppercase letters
#   3. Message following the colon and optional whitespace
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>.*?)\]\s+(?P<level>[A-Z]+):\s+(?P<message>.*)$')

def analyze_log_data(record: str):
    """
    Decode a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the expected format;
        otherwise None.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract groups safely; no further validation is required.
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
        return timestamp, level, message
    except Exception:
        # Any unexpected exception is swallowed to ensure the function never raises.
        return None