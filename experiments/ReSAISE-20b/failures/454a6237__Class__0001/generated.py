import re

# Compile a simple, efficient regular expression that matches a URL starting with
# http:// or https:// followed by any non‑whitespace characters.
_URL_RE = re.compile(r'^(https?://)[^\s]*$', re.IGNORECASE)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether the supplied string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate.

    Returns
    -------
    bool
        True if the string starts with "http://" or "https://"
        and contains only non‑whitespace characters thereafter;
        False otherwise.

    Notes
    -----
    The function uses a pre‑compiled regular expression to avoid the overhead of
    re-compilation on every call. The pattern is intentionally simple and
    linear in the input size to prevent catastrophic backtracking (CWE‑407).
    """
    # Defensive check: ensure the argument is a string
    if not isinstance(path_string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return _URL_RE.fullmatch(path_string) is not None