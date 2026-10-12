import re

# Precompile the regex for performance and safety.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                     # optional leading whitespace
    \[([^]]+)\]              # timestamp inside brackets, capture group 1
    \s*                      # optional whitespace
    (\w+)                    # log level (alphanumeric), capture group 2
    :\s*                     # colon separator with optional whitespace
    (.+?)                    # message, capture group 3 (non-greedy)
    \s*$                     # optional trailing whitespace to end of line
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str):
    """
    Parse a log entry of the form "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters
    ----------
    log_line : str
        The raw log line to parse.

    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the line matches the expected format,
        otherwise None. No exception is raised on invalid input.
    """
    if not isinstance(log_line, str):
        return None

    match = _LOG_PATTERN.match(log_line)
    if not match:
        return None

    # Strip any accidental whitespace around captured groups
    timestamp = match.group(1).strip()
    log_level = match.group(2).strip()
    message = match.group(3).strip()

    return timestamp, log_level, message