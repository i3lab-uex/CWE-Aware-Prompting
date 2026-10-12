import re
from typing import Optional, Tuple

# Pre‑compile the pattern for efficiency and to avoid repeated compilation.
_LOG_PATTERN = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)      # anything up to the closing bracket
    \]\s*
        (?P<level>[A-Z]+):\s*     # log level in uppercase followed by colon
        (?P<message>.*)           # the rest is the message
    """,
    re.VERBOSE,
)


def analyze_log_data(record: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    Optional[Tuple[str, str, str]]
        A tuple containing (timestamp, log_level, message) if the record
        matches the expected format; otherwise ``None``.

    Notes
    -----
    The function is intentionally defensive: it never raises an exception,
    even if the input is malformed or not a string.  It uses a pre‑compiled
    regular expression to avoid repeated compilation overhead and potential
    resource leaks.
    """
    try:
        # Ensure the input is a string; if not, return None gracefully.
        if not isinstance(record, str):
            return None

        match = _LOG_PATTERN.match(record)
        if not match:
            return None

        # Extract groups safely; default to empty strings if any are missing.
        timestamp = match.group('timestamp') or ''
        level = match.group('level') or ''
        message = match.group('message') or ''

        return timestamp, level, message
    except Exception:
        # Swallow any unexpected exception to satisfy the "no exceptions" contract.
        return None