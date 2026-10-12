import re

# Compile the regex once for efficiency.
# This pattern matches a full URL that starts with http:// or https://,
# followed by at least one non‑whitespace character (the rest of the URL).
_URL_RE = re.compile(r'^(https?://)[^\s]+$')

def path_check(u: str) -> bool:
    """
    Validate that `u` is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the URL pattern, False otherwise.

    Notes
    -----
    - The function never raises an exception; any error results in False.
    - The regex is anchored to the start and end of the string, ensuring
      a full match.  It also rejects strings containing whitespace,
      which are not valid in URLs.
    """
    try:
        # Use fullmatch to ensure the entire string matches the pattern.
        return _URL_RE.fullmatch(u) is not None
    except Exception:
        # In the unlikely event of an internal error, treat as invalid.
        return False