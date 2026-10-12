import re

# Pre‑compiled regular expression for a simple HTTP/HTTPS URL.
# It matches:
#   - Scheme: http or https
#   - "://"
#   - At least one non‑whitespace character (the rest of the URL)
_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def path_verification(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP or HTTPS URL, otherwise False.
    The function never raises an exception; invalid inputs simply return False.

    Parameters
    ----------
    link : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the input matches the expected pattern, False otherwise.
    """
    # Defensive programming: ensure the argument is a string
    if not isinstance(link, str):
        return False

    # Use the compiled regex for a quick match
    return bool(_URL_RE.match(link))