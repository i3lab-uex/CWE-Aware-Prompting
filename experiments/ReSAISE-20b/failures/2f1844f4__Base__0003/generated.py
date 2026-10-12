import re

# Regular expression that matches a well‑formed HTTP or HTTPS URL.
# The pattern is deliberately simple and flat to avoid catastrophic backtracking
# (CWE‑1333). It checks the scheme, optional credentials, host and optional path/query
# components. Only characters that are allowed in URLs per RFC 3986 are permitted.
_URL_REGEX = re.compile(
    r'^https?://'                               # http:// or https://
    r'(?:[\w\-]+(?::[\w\-]+)?@)?'               # optional user:pass@
    r'(?:[a-zA-Z0-9\-\.]+|\[[^\]]+\])'          # host (IPv4, domain or IPv6)
    r'(?:\:\d+)?'                               # optional port
    r'(?:/[^\s]*)?$'                            # optional path/query/hash (no whitespace)
)

def is_valid_path(site_path: str) -> bool:
    """
    Return True if *site_path* is a syntactically valid HTTP or HTTPS URL,
    otherwise False.

    The function performs no I/O and never raises an exception.
    """
    if not isinstance(site_path, str):
        return False
    # Strip leading/trailing whitespace to avoid accidental failures.
    site_path = site_path.strip()
    return bool(_URL_REGEX.match(site_path))