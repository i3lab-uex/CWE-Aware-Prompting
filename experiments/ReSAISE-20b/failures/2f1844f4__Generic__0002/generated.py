import re

# Regular expression that matches a basic HTTP/HTTPS URL.
# It requires the scheme, at least one non‑space character for the host,
# and allows any characters after that except whitespace.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme
    [^\s/$.?#].[^\s]*                   # at least one non‑space character for host, then any non‑whitespace
    $                                   # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Return True if `site_path` is a valid HTTP or HTTPS URL, otherwise False.
    
    The function does not raise exceptions for malformed input; it simply
    returns a boolean.  It uses a permissive regular expression that accepts
    typical URLs, but it does not perform full RFC 3986 validation.
    
    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential URL.
    
    Returns
    -------
    bool
        True if `site_path` matches the HTTP/HTTPS pattern, False otherwise.
    """
    if not isinstance(site_path, str):
        return False
    # Strip leading/trailing whitespace to avoid false negatives.
    site_path = site_path.strip()
    return bool(_URL_RE.match(site_path))