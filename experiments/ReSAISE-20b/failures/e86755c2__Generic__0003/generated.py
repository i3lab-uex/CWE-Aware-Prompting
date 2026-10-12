import re

# Regular expression that matches a typical http or https URL.
# It requires the scheme (http:// or https://) followed by at least one non‑space character.
# This is intentionally permissive while still rejecting obvious invalid paths.
_HTTP_URL_RE = re.compile(r'^(https?://)[^\s]+$', re.IGNORECASE)

def verify_link(link: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if `link` matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non‑string inputs; return False without raising an exception.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(link))