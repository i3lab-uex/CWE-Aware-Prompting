import re

# Compile the regular expression once for efficiency and safety.
# The pattern captures:
#   1. Anything inside square brackets as the timestamp (non-greedy).
#   2. A word character sequence as the log level.
#   3. The remaining text after a colon and optional whitespace as the message.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def analyze_log_entry(entry: str):
    """
    Extract timestamp, log level, and message from a log entry.

    Parameters
    ----------
    entry : str
        A string representing the individual log entry in the format:
        '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the expected format,
        otherwise None.
    """
    # Ensure we are working with a string; if not, return None gracefully.
    if not isinstance(entry, str):
        return None

    match = _LOG_PATTERN.match(entry)
    if not match:
        return None

    # Extract captured groups.
    timestamp, log_level, message = match.groups()
    return timestamp, log_level, message