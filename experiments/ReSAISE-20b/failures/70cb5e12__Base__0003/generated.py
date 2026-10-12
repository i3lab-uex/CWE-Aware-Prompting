import re

# Compile the regex once at import time to avoid repeated compilation overhead.
_LOG_ENTRY_RE = re.compile(
    r'^\[(?P<ts>[^]]+?)\]\s*(?P<lvl>\w+):\s*(?P<msg>.+)$',
    re.ASCII
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A 3-tuple containing (timestamp, log_level, message) if the record matches
        the expected format; otherwise None.

    Notes
    -----
    - The function never raises an exception.  Any error in parsing simply results
      in a return value of None.
    - The regular expression is deliberately simple and anchored at the
      beginning (^) and end ($) of the string to avoid catastrophic backtracking.
    - The pattern uses non-greedy matching for the timestamp and a simple
      character class that excludes the closing bracket to keep complexity linear.
    """
    if not isinstance(record, str):
        return None

    match = _LOG_ENTRY_RE.match(record)
    if not match:
        return None

    # Extract named groups safely; they are guaranteed to exist because of the pattern.
    timestamp = match.group('ts')
    log_level = match.group('lvl')
    message = match.group('msg')

    return timestamp, log_level, message