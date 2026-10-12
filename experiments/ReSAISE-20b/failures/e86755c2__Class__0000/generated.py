import re

# A simple, non‑backtracking regex that matches a typical HTTP/HTTPS URL.
# It allows:
#   - optional scheme: http or https
#   - "://"
#   - any non‑whitespace characters (hostname, path, query, fragment)
_URL_RE = re.compile(r'^(https?://[^\s]+)$')

def verify_link(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP/HTTPS URL, otherwise False.
    
    The function performs no network I/O and never raises an exception.
    
    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if `link` matches the expected URL pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False
    # Use fullmatch to ensure the entire string matches the pattern.
    return bool(_URL_RE.fullmatch(link))