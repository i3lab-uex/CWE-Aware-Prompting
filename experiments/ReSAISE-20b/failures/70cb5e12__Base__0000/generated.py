import re

# Compile a safe, non‑backtracking regex once for reuse.
_LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s*(?P<log_level>\w+):\s*(?P<message>.*)$"
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract named groups for clarity.
        timestamp = match.group("timestamp")
        log_level = match.group("log_level")
        message = match.group("message")
        return timestamp, log_level, message
    except Exception:
        # Ensure no exception propagates.
        return None