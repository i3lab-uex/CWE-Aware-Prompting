import re

# Regular expression that captures the timestamp, log level and message.
# It is anchored to the start and end of the string to avoid partial matches.
_LOG_RE = re.compile(
    r"""
    ^\s*                                   # Optional leading whitespace
    \[(?P<timestamp>.+?)\]                 # Timestamp inside brackets (non-greedy)
    \s+                                    # One or more spaces
    (?P<level>[A-Z]+)                      # Log level in uppercase letters
    :\s*                                   # Colon followed by optional spaces
    (?P<message>.*)                        # The rest is the message
    \s*$                                   # Optional trailing whitespace to end of line
    """,
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Decode a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the format matches,
        otherwise None.
    """
    try:
        match = _LOG_RE.match(record)
        if not match:
            return None
        # Extract groups; strip surrounding whitespace for safety.
        timestamp = match.group("timestamp").strip()
        level = match.group("level").strip()
        message = match.group("message").strip()
        return timestamp, level, message
    except Exception:
        # Any unexpected error (e.g., None input) results in a graceful failure.
        return None