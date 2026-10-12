import re

# Pre‑compiled regex for a basic HTTP/HTTPS URL.
# The pattern is intentionally simple to avoid catastrophic backtracking
# (CWE‑1333). It allows the standard characters used in URLs.
_URL_REGEX = re.compile(
    r'^(https?://)[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+$', re.IGNORECASE
)

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
        ``True`` if the string matches the expected pattern, otherwise ``False``.

    Notes
    -----
    The function performs a simple structural check and does not resolve the URL,
    perform DNS lookups, or verify that the host actually exists.  It is designed
    to be safe from regular‑expression denial of service attacks by using a
    straightforward, non‑backtracking pattern.
    """
    if not isinstance(path_string, str):
        return False

    # Strip surrounding whitespace that might have been accidentally added.
    path_string = path_string.strip()

    return bool(_URL_REGEX.match(path_string))