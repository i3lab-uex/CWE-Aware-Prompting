import re

# Pre‑compile a simple, efficient regex for HTTP(S) URLs.
# The pattern matches "http://" or "https://", followed by at least one non‑space character.
# It does **not** attempt to validate the full URL syntax (e.g., domain names, query strings),
# but it is sufficient for typical path validation and avoids pathological backtracking.
_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Return True if *string* is a valid HTTP or HTTPS path, otherwise False.

    The function performs a single full‑match against a pre‑compiled regular expression.
    It is designed to be fast and resistant to excessive backtracking (CWE‑407).

    Parameters
    ----------
    string : str
        The candidate URL to validate.

    Returns
    -------
    bool
        True if *string* matches the HTTP(S) pattern, False otherwise.
    """
    # Guard against non‑string input; silently return False instead of raising an exception.
    if not isinstance(string, str):
        return False

    # Perform a full match; this is O(n) where n = len(string).
    return bool(_URL_RE.fullmatch(string))