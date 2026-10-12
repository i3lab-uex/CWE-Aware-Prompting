import re

# Compile a safe, non-greedy regex pattern to avoid excessive backtracking.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def extract_log_data(log_line: str):
    """
    Extract timestamp, log level and message from a log entry.

    Parameters
    ----------
    log_line : str
        The log line to parse, expected in the form:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A tuple of (timestamp, log_level, message) on success,
        otherwise None if the line does not match the expected format.
    """
    try:
        # Strip leading/trailing whitespace to be tolerant of accidental spaces.
        line = log_line.strip()
    except AttributeError:
        # Non-string input; return None gracefully.
        return None

    match = _LOG_PATTERN.match(line)
    if not match:
        return None

    timestamp, log_level, message = match.groups()
    # Basic sanity checks (e.g., non-empty components).
    if not timestamp or not log_level:
        return None
    # Message may legitimately be empty; allow that.

    return timestamp, log_level, message