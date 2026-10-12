import re

# Compile the pattern once for efficiency and to avoid repeated compilation.
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)   # anything except the closing bracket
    \]\s+
        (?P<level>\w+):\s+
        (?P<message>.*)         # the rest of the line
    $""",
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Decode a log entry of the form "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple | None
        A 3-tuple (timestamp, log_level, message) if the record matches the
        expected format; otherwise None.

    Notes
    -----
    The function never raises an exception.  It returns None for malformed
    input or any internal error (e.g., if the regex fails).  This protects
    against potential denial‑of‑service attacks that exploit catastrophic
    backtracking by ensuring the regex is anchored and uses non‑greedy
    matching.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract named groups for clarity.
        timestamp = match.group("timestamp")
        level = match.group("level")
        message = match.group("message")
        return timestamp, level, message
    except Exception:
        # Silently handle any unexpected errors.
        return None