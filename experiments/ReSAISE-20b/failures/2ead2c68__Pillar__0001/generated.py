import re

# Regular expression that matches a valid HTTP or HTTPS URL.
# It allows optional user:pass@, host (IPv4, IPv6, or domain), optional port,
# path with allowed characters, query string and fragment.
_HTTP_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                                   # scheme
    (?:(?P<userinfo>[^@/\s]+)@)?                            # optional userinfo
    (?P<host>
        \[[^\]]+\]                                          # IPv6 in brackets
        |                                                   # or
        (?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})  # domain
        |                                                   # or IPv4
        (?:\d{1,3}\.){3}\d{1,3}
    )
    (?::(?P<port>\d{1,5}))?                                 # optional port
    (?P<path>/[^\s?#]*)?                                     # path
    (?:\?(?P<query>[^\s#]*))?                                # query string
    (?:\#(?P<fragment>[^\s]*))?$                            # fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def path_verification(link: str) -> bool:
    """
    Validate whether the input string is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    try:
        return _HTTP_URL_RE.match(link) is not None
    except Exception:  # pragma: no cover
        # Defensive catch to avoid leaking any unexpected exception.
        return False