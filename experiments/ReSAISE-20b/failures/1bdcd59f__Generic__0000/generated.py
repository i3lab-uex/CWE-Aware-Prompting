import re

# Regular expression to validate a simple HTTP/HTTPS URL.
# It ensures the string starts with http:// or https://,
# followed by at least one non-whitespace character.
_URL_RE = re.compile(r'^(https?://\S+)$', re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Check if the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against non-string inputs
    if not isinstance(u, str):
        return False

    try:
        # Use fullmatch to ensure the entire string matches the pattern
        return _URL_RE.fullmatch(u) is not None
    except Exception:
        # In case of unexpected errors, return False without raising
        return False