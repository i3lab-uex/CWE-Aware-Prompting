import re

# Pre‑compiled, efficient regular expression for HTTP/HTTPS URLs.
# The pattern matches:
#   * "http://" or "https://"
#   * a host consisting of letters, digits, dots or hyphens
#   * an optional port (e.g., :80)
#   * an optional path/query string that does not contain whitespace
_HTTP_URL_RE = re.compile(
    r'^https?://[A-Za-z0-9.-]+(:\d+)?(/[^\s]*)?$',
    re.IGNORECASE
)

def verify_link(link: str) -> bool:
    """
    Determine whether *link* is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to be evaluated as a potential URL.

    Returns
    -------
    bool
        True if *link* matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against None or non‑string inputs to avoid exceptions
    if not isinstance(link, str):
        return False

    # Use the compiled regex for fast matching
    return bool(_HTTP_URL_RE.match(link))