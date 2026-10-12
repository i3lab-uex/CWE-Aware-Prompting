import re
from typing import Optional, Tuple

# Pre‑compile the regular expression for efficiency and to avoid repeated compilation.
_LOG_RE = re.compile(
    r"""
    ^\s*                         # optional leading whitespace
    \[(?P<timestamp>[^]]+)\]     # timestamp inside brackets, anything but ]
    \s*                          # optional whitespace
    (?P<level>\w+):              # log level followed by a colon
    \s*                          # optional whitespace before message
    (?P<message>.*)              # the rest of the line as the message
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    log_line : str
        The raw log line to parse. Expected format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple of (timestamp, log_level, message) if parsing succeeds,
        otherwise None.

    Notes
    -----
    The function never raises an exception; any error (including
    non‑string input or malformed lines) results in a None return.
    """
    try:
        if not isinstance(log_line, str):
            return None

        match = _LOG_RE.match(log_line)
        if not match:
            return None

        timestamp = match.group("timestamp").strip()
        level = match.group("level").strip()
        message = match.group("message").strip()

        return timestamp, level, message
    except Exception:
        # Any unexpected error should not propagate; simply return None.
        return None