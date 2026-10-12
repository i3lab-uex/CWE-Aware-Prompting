import re

# Compile the regex once at module load time for efficiency and safety.
_LOG_PATTERN = re.compile(
    r'''
    ^\[
        (?P<timestamp>[^]]+)      # everything inside the brackets
    \]\s*
        (?P<level>\w+):           # log level followed by a colon
    \s*
        (?P<message>.+)           # the rest is the message
    $''',
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form '[TIMESTAMP] LOG_LEVEL: MESSAGE'.

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple (timestamp, log_level, message) if the record matches the
        expected format; otherwise None.

    Notes
    -----
    The function never raises an exception.  It safely returns ``None`` for
    malformed input, empty strings, or any other unexpected content.
    """
    if not isinstance(record, str):
        return None
    match = _LOG_PATTERN.match(record)
    if not match:
        return None
    # Return the captured groups in order: timestamp, level, message
    return (
        match.group('timestamp').strip(),
        match.group('level').strip(),
        match.group('message').strip()
    )