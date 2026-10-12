import re

# A compact, efficient regular expression that covers most common URL forms.
# It matches:
#   - Optional scheme (http, https, ftp, ftps) followed by ://
#   - An optional user:password@ part
#   - A host that is either an IPv4 address, a domain name with at least one dot,
#     or the literal "localhost"
#   - Optional port number
#   - An optional path, query or fragment component.
_URL_REGEX = re.compile(
    r"""
    ^                                   # start of string
    (?:                                 # optional scheme
        (?P<scheme>https?|ftps?)://
    )?
    (?:                                 # optional user:pass@
        (?P<user>[^:@/]+)               # username
        (?::(?P<pwd>[^@/]*))?           # optional password
        @
    )?
    (?:                                 # host part
        (?P<ipv4>(?:\d{1,3}\.){3}\d{1,3})  # IPv4
        |
        (?P<domain>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})  # domain
        |
        localhost
    )
    (?::(?P<port>\d{1,5}))?             # optional port
    (?:                                 # optional path/query/fragment
        /[^?#]*                         # path
        (\?[^#]*)?                      # query
        (#.*)?                           # fragment
    )?
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Validate whether the given string is a syntactically correct URL.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the input matches the URL pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False

    match = _URL_REGEX.match(link)
    if not match:
        return False

    # Additional sanity checks for IPv4 octets (0-255)
    ipv4 = match.group("ipv4")
    if ipv4:
        octets = ipv4.split(".")
        for octet in octets:
            if not 0 <= int(octet) <= 255:
                return False

    # Port number must be within valid range if present
    port = match.group("port")
    if port:
        if not 0 <= int(port) <= 65535:
            return False

    return True