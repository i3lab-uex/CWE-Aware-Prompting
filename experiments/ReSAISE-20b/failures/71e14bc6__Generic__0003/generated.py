import re

# Compile the regex once at module load for efficiency and safety.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                           # optional leading whitespace
    \[(?P<timestamp>[^]]+)\]       # timestamp inside brackets
    \s*                            # optional whitespace
    (?P<level>\w+)                 # log level (alphanumeric)
    \s*:\s*                        # colon surrounded by optional whitespace
    (?P<message>.*)                # the rest is the message (can be empty)
    \s*$                           # optional trailing whitespace
    """,
    re.VERBOSE,
)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level, and message from a log entry.

    Parameters
    ----------
    entry : str
        A string representing the individual log entry in the format:
        '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None.

    Notes
    -----
    No exceptions are raised. The function safely returns None on any parsing
    failure or if the input is not a string.
    """
    # Guard against non-string inputs; return None without raising
    if not isinstance(entry, str):
        return None

    match = _LOG_PATTERN.match(entry)
    if not match:
        return None

    # Extract named groups; strip to remove accidental surrounding whitespace
    timestamp = match.group('timestamp').strip()
    level = match.group('level').strip()
    message = match.group('message').strip()

    return timestamp, level, message