import re

# Regular expression that loosely matches a valid HTTP or HTTPS URL.
# It requires:
#   - the scheme (http or https) followed by ://
#   - a domain consisting of letters, digits, dots and hyphens
#   - an optional port number prefixed by :
#   - an optional path/query/fragment that may contain any URL‑safe characters
_URL_RE = re.compile(
    r'^https?://'                                   # http:// or https://
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?\.)+'  # subdomains
    r'[A-Za-z]{2,}'                                 # top‑level domain
    r'(?:\:\d{1,5})?'                               # optional port
    r'(?:[/?#][^\s]*)?$',                          # optional path, query or fragment
    re.IGNORECASE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if `site_path` matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against non‑string input
    if not isinstance(site_path, str):
        return False

    # Strip leading/trailing whitespace to avoid false negatives
    site_path = site_path.strip()

    return bool(_URL_RE.match(site_path))