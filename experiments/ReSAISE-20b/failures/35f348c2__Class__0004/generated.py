import re

# Compile a fast, non‑backtracking regex for HTTP/HTTPS URLs.
# The pattern matches:
#   - protocol: http or https
#   - ://
#   - any number of allowed URL characters (letters, digits, and the
#     set of RFC 3986 unreserved/allowed characters).
# It intentionally avoids optional groups and alternations that could
# lead to catastrophic backtracking.
_URL_RE = re.compile(
    r'^https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+$',
    re.ASCII
)

def validate_path(path: str) -> bool:
    """
    Return True if *path* is a valid HTTP or HTTPS URL, False otherwise.
    The function does not raise exceptions and uses a precompiled regex
    to avoid inefficiencies (CWE‑407).
    
    Parameters
    ----------
    path : str
        The URL string to validate.
    
    Returns
    -------
    bool
        True if *path* matches the pattern, False otherwise.
    """
    # Quick length check to avoid unnecessary regex work on obviously
    # invalid strings (e.g., empty or too short).
    if not path or len(path) < 7:   # "http://"
        return False
    return bool(_URL_RE.match(path))