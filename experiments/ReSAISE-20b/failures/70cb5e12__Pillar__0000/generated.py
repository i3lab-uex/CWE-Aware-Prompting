import re

# Pre‑compiled pattern for performance and safety.
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)   # everything until the closing bracket
    \]\s*
        (?P<level>[A-Z]+)      # log level in uppercase letters
    :\s*
        (?P<message>.*)        # the rest is the message
    $""",
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple or None
        (timestamp, log_level, message) if the format matches;
        otherwise None.

    Notes
    -----
    - No exceptions are raised; malformed input simply yields None.
    - The function is safe against malicious input because the regex
      does not perform backtracking on unbounded quantifiers.
    """
    if not isinstance(record, str):
        return None

    match = _LOG_PATTERN.match(record)
    if not match:
        return None

    # Extract groups safely
    try:
        timestamp = match.group('timestamp')
        level = match.group('level')
        message = match.group('message')
    except Exception:
        # Any unexpected issue results in a graceful failure
        return None

    return timestamp, level, message