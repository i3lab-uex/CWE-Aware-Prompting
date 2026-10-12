import re

# Compile a regex that matches the log format:
#   [TIMESTAMP] LOG_LEVEL: MESSAGE
# Use a non-greedy match for the timestamp and allow any whitespace around separators.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+(\w+):\s+(.*)$', re.DOTALL)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A 3‑tuple of (timestamp, log_level, message) if the entry matches the
        expected format; otherwise None.

    Notes
    -----
    - The function is intentionally defensive: it never raises an exception.
    - `re.DOTALL` allows the message part to contain newlines if present.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # The regex guarantees three capturing groups.
        timestamp, log_level, message = match.group(1), match.group(2), match.group(3)
        return timestamp, log_level, message
    except Exception:
        # Any unexpected error results in a safe fallback.
        return None