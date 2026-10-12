import re

# Compile the pattern once at module load time to avoid repeated compilation overhead.
_LOG_ENTRY_PATTERN = re.compile(
    r'^\[(?P<timestamp>[^\]]+)\]\s+(?P<level>\w+):\s*(?P<message>.*)$'
)

def analyze_log_entry(entry: str):
    """
    Extracts the timestamp, log level and message from a log entry string.
    
    Parameters
    ----------
    entry : str
        A single log line expected to follow the format:
            [TIMESTAMP] LOG_LEVEL: MESSAGE
        
    Returns
    -------
    tuple | None
        A tuple (timestamp, log_level, message) if the entry matches the pattern,
        otherwise None.
    
    Notes
    -----
    - The function never raises an exception; any failure to match simply returns None.
    - The regular expression is compiled once at import time, preventing
      resource leaks associated with repeated compilation.
    """
    if not isinstance(entry, str):
        return None

    match = _LOG_ENTRY_PATTERN.match(entry)
    if not match:
        return None

    timestamp = match.group('timestamp')
    level = match.group('level')
    message = match.group('message')

    return timestamp, level, message