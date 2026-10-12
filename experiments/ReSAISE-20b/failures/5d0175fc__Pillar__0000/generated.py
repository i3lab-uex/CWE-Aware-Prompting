import re

# Regular expression for a basic HTTP/HTTPS URL.
# It matches the scheme, host (with optional port), and path/query/fragment.
_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                                 # http or https scheme
    (?:(?P<user>[^:@/]+)(?::(?P<pwd>[^@/]*))?@)?          # optional user:pass@
    (?P<host>
        \[
            [A-Fa-f0-9:]+                                 # IPv6 literal
        \]
        |
        (?P<hostname>
            (?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*   # subdomains
            [a-zA-Z]{2,}                                       # TLD
        )
    )
    (?::(?P<port>\d{1,5}))?                               # optional port
    (?P<path>/[^\s?#]*)?                                  # path
    (?:\?(?P<query>[^\s#]*))?                             # query string
    (?:\#(?P<fragment>[^\s]*))?$                          # fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify whether the given string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The input string to validate as a path.

    Returns
    -------
    bool
        True if the address matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Guard against None or non-string inputs
    if not isinstance(address, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    match = _URL_RE.fullmatch(address.strip())
    return bool(match)