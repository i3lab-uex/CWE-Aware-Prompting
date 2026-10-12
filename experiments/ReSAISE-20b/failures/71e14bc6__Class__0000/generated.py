import re

# Compile the pattern once for efficiency and to avoid catastrophic backtracking.
_LOG_ENTRY_RE = re.compile(
    r"^\[([^\]]+)\]\s+(\w+):\s+(.*)$",
    re.ASCII
)

def analyze_log_entry(entry: str):
    """
    Extract the timestamp, log level and message from a log entry.

    Parameters
    ----------
    entry : str
        A single line of log text in the form:
            [TIMESTAMP] LOG_LEVEL: MESSAGE

    Returns
    -------
    tuple[str, str, str] | None
        A tuple containing (timestamp, log_level, message) if the entry matches the expected format.
        Returns None if parsing fails.

    Notes
    -----
    - The function never raises an exception; invalid input simply yields ``None``.
    - The regular expression is anchored to the start (^) and end ($) of the string,
      preventing catastrophic backtracking and ensuring O(n) complexity.
    """
    match = _LOG_ENTRY_RE.match(entry)
    if not match:
        return None
    # Return the captured groups as a tuple.
    return match.group(1), match.group(2), match.group(3)