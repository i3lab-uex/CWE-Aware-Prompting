import re
from typing import Optional, Tuple

# Pre-compiled regular expression for efficiency and safety.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                            # Optional leading whitespace
    \[                              # Opening bracket for timestamp
    (?P<timestamp>[^]]+)            # Capture everything until closing bracket
    \]\s*                           # Closing bracket and optional whitespace
    (?P<level>[A-Z]+)               # Log level (uppercase letters only)
    :\s*                            # Colon separator and optional whitespace
    (?P<message>.+?)                # Non-greedy capture of the message
    \s*$                            # Optional trailing whitespace to end of line
    """,
    re.VERBOSE,
)

def extract_log_data(log_line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log line in the format "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Parameters:
        log_line (str): The log entry string to be parsed.

    Returns:
        Optional[Tuple[str, str, str]]: A tuple (timestamp, log_level, message)
            if parsing succeeds; otherwise None.

    Notes:
        - The function never raises exceptions. Any errors are caught and
          result in a None return value.
        - The regex is pre-compiled for performance and to avoid repeated
          compilation overhead.
    """
    try:
        if not isinstance(log_line, str):
            return None
        match = _LOG_PATTERN.match(log_line)
        if not match:
            return None
        timestamp = match.group("timestamp").strip()
        level = match.group("level").strip()
        message = match.group("message").strip()
        return timestamp, level, message
    except Exception:
        # Any unexpected exception results in a graceful None return.
        return None