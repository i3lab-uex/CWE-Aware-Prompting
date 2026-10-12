import re

# Pre-compile a safe, efficient regular expression that matches the log format.
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)   # Anything except the closing bracket
    \]\s+                       # Closing bracket followed by whitespace
        (?P<level>\w+)         # Log level (alphanumeric characters)
    :\s+
        (?P<message>.+)         # The rest of the line as message
    $                           # End of string
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str):
    """
    Extract timestamp, log level and message from a log entry.

    Parameters
    ----------
    log_line : str
        The log entry string to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) on success; otherwise None.
    """
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    timestamp = match.group("timestamp")
    level = match.group("level")
    message = match.group("message")

    return timestamp, level, message