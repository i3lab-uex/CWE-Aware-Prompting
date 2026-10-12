import re

# A simple, non‑backtracking regex that matches typical HTTP/HTTPS URLs.
# It allows any character except whitespace after the scheme and two slashes.
_HTTP_URL_RE = re.compile(r'^(https?)://[^\s]+$', re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Return True if *string* is a valid HTTP or HTTPS URL path, False otherwise.
    The function never raises an exception and uses a simple regex that is
    not vulnerable to catastrophic backtracking (CWE‑1333).

    Parameters
    ----------
    string : str
        The input string to validate.

    Returns
    -------
    bool
        True if *string* matches the pattern, False otherwise.
    """
    # Guard against non‑string inputs; treat them as invalid without raising.
    if not isinstance(string, str):
        return False

    # Perform a full match to ensure the entire string conforms.
    return bool(_HTTP_URL_RE.fullmatch(string))