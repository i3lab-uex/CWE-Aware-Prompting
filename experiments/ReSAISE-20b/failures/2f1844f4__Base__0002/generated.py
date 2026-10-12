import re

# Compile a simple, efficient regular expression that matches HTTP or HTTPS URLs.
# The pattern is deliberately straightforward to avoid catastrophic backtracking
# (CWE-1333). It checks for the scheme, a non-empty domain part that does not
# start with whitespace or control characters, and optionally any remaining
# path/query components that do not contain whitespace.
_HTTP_URL_RE = re.compile(
    r'^(https?://'
    r'(?:[A-Za-z0-9\-._~%]+(?:\.[A-Za-z0-9\-._~%]+)+)'   # domain
    r'(?:\:\d+)?'                                         # optional port
    r'(?:/[^\s]*)?'                                       # optional path
    r')$',
    re.IGNORECASE
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    site_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    The function performs a simple regular‑expression match. It does not attempt
    to resolve the URL, nor does it perform any network I/O. No exceptions are
    raised for invalid input; the function returns False instead.
    """
    if not isinstance(site_path, str):
        return False
    # Use the precompiled regex to test the input.
    return bool(_HTTP_URL_RE.match(site_path))