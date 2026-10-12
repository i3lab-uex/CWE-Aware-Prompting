import re

# Regular expression that matches a valid HTTP or HTTPS URL.
# It allows an optional scheme (http:// or https://) followed by a non‑empty
# sequence of characters that does not contain whitespace.
_HTTP_URL_RE = re.compile(r'^(https?://)?[^\s]+$')

def path_check(u: str) -> bool:
    """
    Check whether the given string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    - The function never raises an exception; it returns False for any
      malformed input.
    - It uses a simple regular expression that only checks the overall
      format; it does not perform DNS resolution or any network access.
    """
    if not isinstance(u, str):
        return False
    # Strip any leading/trailing whitespace to avoid accidental matches.
    u = u.strip()
    return bool(_HTTP_URL_RE.fullmatch(u))