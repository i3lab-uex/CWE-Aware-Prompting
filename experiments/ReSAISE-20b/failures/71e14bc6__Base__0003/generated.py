import re

# Pre‑compile a safe, non‑greedy regular expression for parsing log entries.
_LOG_PATTERN = re.compile(r'^\[(.*?)\]\s+([A-Z]+):\s+(.*)$')

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        A single log line in the format "[TIMESTAMP] LOG_LEVEL: MESSAGE".

    Returns
    -------
    tuple | None
        A 3‑tuple (timestamp, log_level, message) if the entry matches,
        otherwise ``None``.
    """
    match = _LOG_PATTERN.match(entry)
    if not match:
        return None
    # The pattern guarantees three groups: timestamp, level, message.
    return match.group(1), match.group(2), match.group(3)