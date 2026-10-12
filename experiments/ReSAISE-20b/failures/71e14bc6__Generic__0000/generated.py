import re

# Precompile the regex for efficiency and to avoid repeated compilation.
_LOG_PATTERN = re.compile(r'^\[(?P<timestamp>.+?)\]\s+(?P<level>\w+):\s*(?P<message>.+)$')

def analyze_log_entry(entry: str):
    """
    Extracts the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        A single log line in the format "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Returns
    -------
    tuple | None
        A 3‑tuple (timestamp, log_level, message) if the entry matches the pattern,
        otherwise None. No exception is raised for malformed input.

    Notes
    -----
    - The function uses a compiled regular expression for speed.
    - It is tolerant of additional whitespace between the components.
    - It accepts any non‑empty timestamp and message; log level must be a word
      (letters, digits or underscore).
    """
    if not isinstance(entry, str):
        # Defensive check: return None for non‑string inputs.
        return None

    match = _LOG_PATTERN.match(entry)
    if not match:
        return None

    # Extract named groups for clarity.
    timestamp = match.group('timestamp')
    level = match.group('level')
    message = match.group('message')

    return timestamp, level, message