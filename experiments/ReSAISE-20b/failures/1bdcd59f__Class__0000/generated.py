import re

# Pre‑compiled regular expression for a simple http/https path.
# The pattern matches:
#   * optional "http://" or "https://"
#   * a non‑empty sequence of characters that are not whitespace.
# It is intentionally simple to avoid catastrophic backtracking (CWE‑407).
_HTTP_PATH_RE = re.compile(r'^https?://\S+$', flags=re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Check whether the input string is a valid http or https path.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the http/https path pattern, False otherwise.

    Notes
    -----
    The function never raises exceptions.  It returns ``False`` for any input
    that is not a string or does not match the pattern.
    """
    if not isinstance(u, str):
        return False
    # Using fullmatch ensures the entire string must match the pattern.
    return bool(_HTTP_PATH_RE.fullmatch(u))