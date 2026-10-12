import re

# Regular expression to validate a simple HTTP/HTTPS path.
# It ensures the string starts with http:// or https://, followed by at least one
# non-whitespace character. The pattern is intentionally simple to avoid catastrophic
# backtracking while still covering the typical use case.
_PATH_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Validate whether the input string is a syntactically valid HTTP or HTTPS URL path.

    Parameters
    ----------
    string : str
        The candidate URL string to validate.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.

    Notes
    -----
    The function is defensive: it never raises an exception. Any unexpected input or
    internal error results in a False return value.
    """
    try:
        # Use fullmatch to ensure the entire string conforms to the pattern.
        return bool(_PATH_RE.fullmatch(string))
    except Exception:
        # In case of any unforeseen error, return False rather than propagating.
        return False