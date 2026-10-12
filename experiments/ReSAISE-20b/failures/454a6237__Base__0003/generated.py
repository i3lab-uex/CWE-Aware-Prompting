import re

# Compile the regex once at import time for efficiency.
# The pattern matches:
#   - http:// or https://
#   - a non-empty hostname (letters, digits, hyphens, dots)
#   - optional port
#   - optional path/query/fragment
# This pattern avoids nested quantifiers, preventing catastrophic backtracking.
_HTTP_URL_RE = re.compile(
    r'^https?://'                      # http:// or https://
    r'(?:(?:[a-zA-Z0-9\-]+\.)+'        # subdomains and domain
    r'[a-zA-Z]{2,})'                   # top‑level domain
    r'(?:\:\d{1,5})?'                  # optional port
    r'(?:[/?#][^\s]*)?$',              # optional path, query or fragment
    re.IGNORECASE
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether `path_string` is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Defensive programming: ensure the input is a string.
    if not isinstance(path_string, str):
        return False

    # The regex search is O(n) and safe from backtracking.
    return bool(_HTTP_URL_RE.match(path_string))