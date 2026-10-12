import re
from typing import Optional, Tuple

# Pre‑compiled regular expression for performance and safety.
_LOG_ENTRY_RE: re.Pattern = re.compile(
    r"""
    ^\s*                                # Optional leading whitespace
    \[(?P<timestamp>[^\]]+)\]           # Timestamp inside brackets
    \s*                                 # Optional whitespace
    (?P<level>[A-Z]+)                   # Log level (uppercase letters)
    \s*:\s*                             # Colon surrounded by optional whitespace
    (?P<message>.*)                     # The rest is the message
    \s*$                                # Optional trailing whitespace
    """,
    re.VERBOSE,
)

def analyze_log_entry(entry: str) -> Optional[Tuple[str, str, str]]:
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The log entry string in the format '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None.

    Notes
    -----
    - The function never raises an exception. If the input does not match,
      it simply returns None.
    - The regular expression is compiled once at import time for efficiency
      and to avoid repeated compilation overhead.
    """
    if not isinstance(entry, str):
        return None

    match = _LOG_ENTRY_RE.match(entry)
    if not match:
        return None

    timestamp = match.group("timestamp")
    level = match.group("level")
    message = match.group("message")

    return timestamp, level, message