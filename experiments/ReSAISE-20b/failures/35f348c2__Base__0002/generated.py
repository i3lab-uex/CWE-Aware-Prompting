import re

# Compile a simple, non‑backtracking regex for HTTP/HTTPS URLs.
# The pattern matches:
#   - scheme: http or https
#   - ://
#   - host: any non‑space characters that include at least one dot or a port
#   - optional path, query and fragment.
_URL_RE = re.compile(
    r"""
    ^                             # start of string
    https?://                     # http or https scheme followed by ://
    [^\s/]+(?:\.[^\s/]*)+         # host part with at least one dot
    (?:\:\d+)?                    # optional port
    [^\s]*                        # rest of the URL (path, query, fragment)
    $                             # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def validate_path(path: str) -> bool:
    """
    Validate that the given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if `path` is a valid HTTP/HTTPS URL, False otherwise.
    """
    # Ensure the input is a string; if not, return False without raising.
    if not isinstance(path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return _URL_RE.fullmatch(path) is not None