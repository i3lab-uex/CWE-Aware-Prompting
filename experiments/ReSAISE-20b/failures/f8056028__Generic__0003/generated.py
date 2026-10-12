import re

# Pre‑compile the regular expression for efficiency and safety.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                     # Optional leading whitespace
    \[ (?P<timestamp> [^\]]+ ) \]   # Timestamp inside brackets
    \s*                      # Optional whitespace
    (?P<level> \w+ )         # Log level (word characters)
    :\s*                     # Colon followed by optional whitespace
    (?P<message> .+ )        # The rest is the message
    \s*$                     # Optional trailing whitespace and end of line
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str):
    """
    Parse a log line of the form "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters
    ----------
    log_line : str
        The raw log entry.

    Returns
    -------
    tuple | None
        A 3‑tuple (timestamp, log_level, message) on success.
        If the line does not match the expected format or an error occurs,
        None is returned.

    Notes
    -----
    The function never raises exceptions; it simply returns ``None`` on
    failure, which keeps the caller logic simple and avoids leaking
    information about the internal parsing process.
    """
    try:
        if not isinstance(log_line, str):
            return None

        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None

        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')

        # Basic sanity checks to avoid empty components
        if not (timestamp and level and message):
            return None

        return timestamp, level, message
    except Exception:
        # Catch any unforeseen exception to satisfy the no‑raise contract.
        return None