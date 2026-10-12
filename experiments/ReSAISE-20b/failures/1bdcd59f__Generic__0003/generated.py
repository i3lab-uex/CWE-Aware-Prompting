import re

# Regular expression that matches a typical HTTP or HTTPS URL.
# It allows:
#   - scheme: http:// or https://
#   - optional user info, host (IP or domain), optional port
#   - path, query and fragment parts
URL_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme
    (?:[A-Za-z0-9\-._~%]+@)?    # optional user:pass@
    (?:                         # host part
        \d{1,3}(?:\.\d{1,3}){3} # IPv4
        |
        (?:[A-Za-z0-9\-._~%]+:)* # IPv6 brackets are omitted for brevity
        [A-Za-z0-9\-._~%]+      # domain name
    )
    (?::\d{1,5})?               # optional port
    (?:/[^\\s?#]*)*             # path, query and fragment
    $                           # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def path_check(u: str) -> bool:
    """
    Return True if the input string is a valid HTTP or HTTPS URL, otherwise False.
    
    Parameters
    ----------
    u : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if `u` matches the URL pattern, False otherwise.
    
    Notes
    -----
    The function never raises an exception; it simply returns False for any
    input that does not conform to the pattern.
    """
    if not isinstance(u, str):
        return False
    return bool(URL_RE.match(u))