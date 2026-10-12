import re
from typing import Optional, Tuple

# Compile the regex once at module load time.  Use a non‑greedy match for
# the timestamp and anchor the pattern to the start/end of the string.
_LOG_PATTERN = re.compile(
    r'^\[(?P<timestamp>[^]]+)\]\s+(?P<level>\w+):\s*(?P<message>.*)$'
)

def analyze_log_entry(entry: str) -> Optional[Tuple[str, str, str]]:
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The raw log entry string in the format
        "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if the entry
        matches the expected format; otherwise None.

    Notes
    -----
    - The function is intentionally defensive: it returns ``None`` on
      any parsing error and never raises an exception.
    - The regular expression is anchored to the entire string to avoid
      partial matches and mitigates potential catastrophic backtracking.
    """
    try:
        match = _LOG_PATTERN.match(entry)
        if not match:
            return None
        return (
            match.group('timestamp'),
            match.group('level'),
            match.group('message')
        )
    except Exception:
        # Swallow any unexpected errors to satisfy the "no exceptions"
        # requirement.
        return None