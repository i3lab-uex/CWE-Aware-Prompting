import re

# Pre‑compile a safe, anchored regex pattern.
# It captures:
#   1. Timestamp enclosed in square brackets
#   2. Log level followed by a colon and a space
#   3. The message (rest of the line)
_LOG_ENTRY_RE = re.compile(
    r"""
    ^\[
        (?P<timestamp>[^]]+)   # anything up to the closing bracket
    \]\s*
        (?P<level>[A-Z]+)      # log level (uppercase letters)
    :\s*
        (?P<message>.*)        # message (any characters, including none)
    $""",
    re.VERBOSE
)

def analyze_log_entry(entry: str):
    """
    Extract timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        The log entry string to parse. Expected format:
        "[TIMESTAMP] LOG_LEVEL: MESSAGE"

    Returns
    -------
    tuple[str, str, str] | None
        A tuple (timestamp, log_level, message) if the entry matches,
        otherwise None.

    Notes
    -----
    - No exceptions are raised; malformed entries simply return None.
    - The regex is anchored to avoid catastrophic backtracking and
      therefore mitigates CWE‑407 concerns.
    """
    match = _LOG_ENTRY_RE.match(entry)
    if not match:
        return None
    # Retrieve named groups for clarity.
    timestamp = match.group("timestamp")
    log_level = match.group("level")
    message = match.group("message")
    return timestamp, log_level, message