import re

# Pre‑compile the pattern for efficiency and to avoid re-compiling on every call.
_LOG_PATTERN = re.compile(
    r"""
    ^\s*                           # Optional leading whitespace
    \[ (?P<timestamp> [^\]]+ )\]   # Timestamp inside brackets
    \s*                            # Optional whitespace after timestamp
    (?P<level> [A-Z]+ )            # Log level (uppercase letters)
    :\s*                           # Colon separator with optional whitespace
    (?P<message> .* )              # The rest of the line as message
    $                              # End of string
    """,
    re.VERBOSE,
)

def analyze_log_data(record: str):
    """
    Parse a log entry of the form:
        [TIMESTAMP] LOG_LEVEL: MESSAGE

    Parameters
    ----------
    record : str
        The log entry string to parse.

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches
        the expected format; otherwise None.

    Notes
    -----
    The function is defensive: it catches any unexpected exceptions and
    guarantees that no exception propagates to the caller.  No external
    resources are opened or held, so there is no risk of CWE‑664.
    """
    try:
        match = _LOG_PATTERN.match(record)
        if not match:
            return None
        # Extract groups safely; they are guaranteed to exist due to the pattern.
        timestamp = match.group('timestamp')
        log_level = match.group('level')
        message = match.group('message')
        return timestamp, log_level, message
    except Exception:
        # Swallow all exceptions to ensure the function never raises.
        return None