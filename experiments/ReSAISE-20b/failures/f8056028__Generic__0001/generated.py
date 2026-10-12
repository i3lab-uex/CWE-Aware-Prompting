import re

# Compile the regular expression once for efficiency and security.
_LOG_RE = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The log entry to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the line matches the expected format,
        otherwise None. No exceptions are raised during parsing.
    """
    if not isinstance(log_line, str):
        # Non-string input cannot be parsed; return None safely.
        return None

    match = _LOG_RE.match(log_line)
    if not match:
        return None

    # Extract captured groups.
    timestamp, log_level, message = match.groups()

    # Basic sanity checks: ensure none of the parts are empty.
    if not timestamp or not log_level or not message:
        return None

    return (timestamp, log_level, message)