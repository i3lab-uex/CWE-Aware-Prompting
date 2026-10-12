import re

# Compile the regex once to avoid repeated compilation overhead.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>.*?)\]\s+(?P<level>\w+):\s+(?P<message>.*)$')

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    log_line : str
        The raw log entry string.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the line matches.
        If parsing fails or input is invalid, None is returned.

    Notes
    -----
    * The function never raises an exception.
    * Uses a compiled regular expression for efficiency and to mitigate
      potential backtracking attacks (CWE‑407).
    """
    try:
        if not isinstance(log_line, str):
            return None
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        return (
            match.group('timestamp'),
            match.group('level'),
            match.group('message')
        )
    except Exception:
        # Catch any unexpected errors to satisfy the no‑exception contract.
        return None