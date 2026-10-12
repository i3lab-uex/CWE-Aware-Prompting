import re

# Compile a safe, non‑backtracking regex once.
_LOG_PATTERN = re.compile(
    r'^\[(?P<ts>.+?)\]\s+(?P<lvl>\w+):\s*(?P<msg>.*)$'
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry to parse.

    Returns
    -------
    tuple or None
        (timestamp, log_level, message) if the entry matches the expected format,
        otherwise None.

    Notes
    -----
    - The function is intentionally defensive: it never raises exceptions.
    - A non‑greedy match (`.+?`) ensures the regex is linear in the input length,
      mitigating CWE‑1333 concerns about catastrophic backtracking.
    """
    if not isinstance(record, str):
        return None

    match = _LOG_PATTERN.match(record)
    if not match:
        return None

    # Extract groups safely
    ts = match.group('ts')
    lvl = match.group('lvl')
    msg = match.group('msg')

    return ts, lvl, msg