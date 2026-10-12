import re

# Precompiled regex for matching a valid HTTP or HTTPS URL.
# The pattern allows:
#   - Scheme: http or https
#   - Optional user:pass authentication
#   - Hostname (IPv4, IPv6, or domain)
#   - Optional port
#   - Path, query and fragment components
_HTTP_URL_REGEX = re.compile(
    r"""
    ^                                   # start of string
    (?P<scheme>https?)://                # http or https scheme
    (?:[^:@\s]+(?::[^@\s]*)?@)?          # optional user:pass@
    (?P<host>
        \[?[A-Za-z0-9\.\-]+(?:\.[A-Za-z]{2,})?\]?   # hostname or IPv4
        |                                    # OR
        \d{1,3}(?:\.\d{1,3}){3}                # IPv4
    )
    (?::\d{1,5})?                        # optional port
    (?:/[^\s]*)?                         # optional path and query/fragment
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if `link` matches the predefined HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    - The function never raises an exception; invalid input types result in False.
    - Uses a precompiled regex to avoid recompilation overhead.
    """
    if not isinstance(link, str):
        return False
    # Strip surrounding whitespace to avoid accidental mismatches.
    link = link.strip()
    return bool(_HTTP_URL_REGEX.match(link))