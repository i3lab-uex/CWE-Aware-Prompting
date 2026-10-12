import re

# Pre‑compile a simple, non‑backtracking regex for http/https URLs.
# It matches:
#   * scheme: "http" or "https"
#   * ://
#   * a non‑empty host/path fragment without whitespace
_URL_REGEX = re.compile(r'^(https?://)[^\s]+$', re.IGNORECASE)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether a given string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the pattern for an HTTP/HTTPS URL,
        False otherwise.

    Notes
    -----
    - The function performs a single full match against a pre‑compiled
      regular expression, ensuring O(n) time complexity.
    - No exceptions are raised; invalid input simply returns False.
    """
    if not isinstance(path_string, str):
        return False
    # Full match ensures the entire string is consumed.
    return bool(_URL_REGEX.fullmatch(path_string))