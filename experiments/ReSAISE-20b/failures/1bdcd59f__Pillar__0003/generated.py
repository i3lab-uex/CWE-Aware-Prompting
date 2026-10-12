import re

# Regular expression for a simple HTTP/HTTPS path validation.
# It matches URLs that start with http:// or https:// followed by
# a valid hostname (letters, digits, hyphens, dots) and an optional path.
_HTTP_PATH_RE = re.compile(
    r'^(https?://)'                     # http:// or https://
    r'(?:(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})'  # domain
    r'(?:/[^\s]*)?$',                 # optional path, no whitespace
    re.IGNORECASE
)

def path_check(u: str) -> bool:
    """
    Validate that the input string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    u : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the input matches the expected pattern, False otherwise.
    """
    # Guard against non-string inputs and empty strings
    if not isinstance(u, str) or not u:
        return False

    # Perform a single regex match
    return bool(_HTTP_PATH_RE.match(u))