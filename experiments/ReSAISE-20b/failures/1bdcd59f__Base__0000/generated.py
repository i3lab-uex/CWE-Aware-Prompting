import re

# A simple, efficient regular expression for validating http/https URLs.
# It ensures the string starts with http:// or https:// and is followed by
# one or more non‑whitespace characters. This pattern avoids backtracking
# pitfalls and is safe from CWE‑1333.
_HTTP_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Validate whether a string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against non‑string input and avoid raising exceptions
    if not isinstance(u, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_HTTP_URL_RE.fullmatch(u))