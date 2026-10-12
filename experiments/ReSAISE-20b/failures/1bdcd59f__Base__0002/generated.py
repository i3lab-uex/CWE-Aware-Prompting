import re

# A simple, safe regex that matches a URL starting with http:// or https://,
# followed by at least one non‑space character.  This pattern avoids
# backtracking pitfalls and is O(n) in the length of the string.
_HTTP_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Check whether a given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    # Guard against non‑string input
    if not isinstance(u, str):
        return False

    # The regex is precompiled; a simple match call is O(n) and
    # cannot cause exponential blow‑up.
    return bool(_HTTP_URL_RE.match(u))