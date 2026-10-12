import re

# Precompile the regex for performance and safety
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+?)          # everything up to the closing bracket
    \]\s*
        (?P<level>[A-Z]+):\s*          # log level (uppercase letters) followed by colon
        (?P<message>.*)$               # the rest of the line is the message
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str):
    """
    Extract timestamp, log level and message from a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    log_line : str
        The log entry to parse.

    Returns
    -------
    tuple[str, str, str] | None
        (timestamp, log_level, message) if parsing succeeds; otherwise None.
    """
    try:
        # Ensure the input is a string
        if not isinstance(log_line, str):
            return None

        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None

        # Extract named groups
        timestamp = match.group("timestamp").strip()
        level = match.group("level").strip()
        message = match.group("message").strip()

        # Basic validation: timestamp and level should not be empty
        if not timestamp or not level:
            return None

        return (timestamp, level, message)
    except Exception:
        # Any unexpected error should not propagate; return None
        return None