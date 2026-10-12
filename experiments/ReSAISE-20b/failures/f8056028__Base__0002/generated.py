import re

# Precompile the regex for efficiency and to avoid repeated compilation.
_LOG_RE = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$')

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The log entry string to be parsed.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) on success,
        or ``None`` if parsing fails or the input is invalid.

    Notes
    -----
    The function never raises exceptions; it returns ``None`` on any error.
    """
    if not isinstance(log_line, str) or not log_line:
        return None

    match = _LOG_RE.match(log_line)
    if not match:
        return None

    # Extract groups and strip any surrounding whitespace
    timestamp, log_level, message = match.groups()
    return timestamp.strip(), log_level.strip(), message.strip()