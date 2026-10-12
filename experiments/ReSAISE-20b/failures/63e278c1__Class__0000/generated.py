import re

# Pre-compiled, non-greedy regex that matches a simple HTTP/HTTPS URL.
# It avoids catastrophic backtracking by using explicit character classes
# and anchors.  The pattern is intentionally simple to prevent excessive
# complexity while still covering typical use cases.
_HTTP_URL_RE = re.compile(
    r"^https?://[^\s/$.?#].[^\s]*$",
    re.IGNORECASE | re.ASCII
)

def check_path(string: str) -> bool:
    """
    Validate whether the input string is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    string : str
        The input string to validate as a URL path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against None or non-string inputs; return False rather than raising.
    if not isinstance(string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _HTTP_URL_RE.fullmatch(string)
    return bool(match)