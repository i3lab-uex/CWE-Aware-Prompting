import re

# Regular expression to match log entries of the form:
# [TIMESTAMP] LOG_LEVEL: MESSAGE
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>.+?)          # non-greedy match for timestamp
    \]\s+
        (?P<log_level>[A-Z]+)       # log level in uppercase letters
    :\s+
        (?P<message>.*)             # message (can contain anything)
    $""",
    re.VERBOSE,
)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The log line to parse. Expected format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A 3-tuple (timestamp, log_level, message) if the entry matches the
        expected format; otherwise None.
    """
    try:
        match = _LOG_PATTERN.fullmatch(entry)
        if not match:
            return None
        return (
            match.group("timestamp"),
            match.group("log_level"),
            match.group("message"),
        )
    except Exception:
        # Any unexpected error (e.g., invalid regex usage) results in None
        return None