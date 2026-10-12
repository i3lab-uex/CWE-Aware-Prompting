import re

# Compile the regex once at import time to avoid repeated compilation.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                           # Optional leading whitespace
    \[(?P<timestamp>.+?)\]         # Timestamp inside brackets, non-greedy
    \s+                            # One or more spaces
    (?P<level>[A-Z]+)              # Log level (uppercase letters)
    :\s*                           # Colon followed by optional spaces
    (?P<message>.*)                # Rest of the line as message
    \s*$                           # Optional trailing whitespace till end
    """,
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry string to be parsed.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format.  Otherwise returns None.

    Notes
    -----
    - The function is intentionally defensive: it never raises an exception.
      Any error (e.g., None input, unexpected format) results in a return value
      of None.
    - The compiled regular expression is reused for every call, preventing
      repeated allocation of regex objects and mitigating resource exhaustion.
    """
    if not isinstance(record, str):
        return None

    match = _LOG_PATTERN.match(record)
    if not match:
        return None

    # Extract groups; strip whitespace from message to be safe.
    timestamp = match.group('timestamp')
    level = match.group('level')
    message = match.group('message').strip()

    return timestamp, level, message