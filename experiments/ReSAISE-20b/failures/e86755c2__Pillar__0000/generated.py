import re

# Regular expression to match a basic HTTP or HTTPS URL.
# It allows any non-whitespace characters after the scheme,
# but does not perform exhaustive validation of hostnames or paths.
_HTTP_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)

def verify_link(link: str) -> bool:
    """
    Determine whether a given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Ensure the input is a string; if not, treat as invalid without raising an exception.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    match = _HTTP_URL_RE.fullmatch(link)
    return bool(match)