import re

# Regular expression that matches a typical HTTP or HTTPS URL.
# It ensures the scheme is http or https, followed by ://,
# then a non‑empty host part (not starting with whitespace or special chars),
# and optionally any path/query/fragment.
_URL_RE = re.compile(
    r'^(https?)://'
    r'(?:[^\s/$.?#]|[a-zA-Z0-9\-._~%]+)+'
    r'(?:/[^\s]*)?$', re.IGNORECASE
)

def check_path(string: str) -> bool:
    """
    Validate that the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    string : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against non-string inputs
    if not isinstance(string, str):
        return False

    try:
        return bool(_URL_RE.match(string))
    except Exception:  # pragma: no cover
        # Any unexpected error results in False, not raising.
        return False