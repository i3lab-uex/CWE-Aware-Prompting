import re

# A simple, non‑backtracking regex that matches a valid HTTP/HTTPS URL.
# It allows any characters except whitespace in the path/query part,
# which is sufficient for most practical purposes and avoids
# catastrophic backtracking.
_URL_RE = re.compile(r'^https?://[^\s]+$')

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate.

    Returns
    -------
    bool
        True if the input matches the expected URL pattern, False otherwise.
    """
    # Guard against None or non-string inputs; return False without raising.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))