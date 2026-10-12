import re

# Pre‑compile the regex for performance and safety.
_LOG_RE = re.compile(
    r"""
    ^\s*                       # Optional leading whitespace
    \[                         # Opening bracket for timestamp
    (?P<timestamp>[^]]+)       # Anything until the closing bracket
    \]\s*                      # Closing bracket and optional whitespace
    (?P<level>\w+):            # Log level (word characters) followed by colon
    \s*                        # Optional whitespace after colon
    (?P<message>.*)            # Rest of the line as message (can be empty)
    """,
    re.VERBOSE
)

def extract_log_data(log_line: str):
    """
    Extracts the timestamp, log level and message from a log entry.

    Parameters
    ----------
    log_line : str
        Log entry string that follows the format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the line matches,
        otherwise None. No exception is raised for malformed input.
    """
    try:
        match = _LOG_RE.match(log_line)
        if not match:
            return None
        timestamp = match.group('timestamp').strip()
        level = match.group('level').strip()
        message = match.group('message').rstrip()  # Preserve leading spaces in message
        return timestamp, level, message
    except Exception:
        # Any unexpected error (unlikely with the regex) results in None.
        return None