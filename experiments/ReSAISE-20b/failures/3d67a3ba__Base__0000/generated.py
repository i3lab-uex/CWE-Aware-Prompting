import re

# A reasonably strict, but efficient URL validator.
# It checks for a scheme (http/https), an optional userinfo,
# host (IPv4, IPv6 or hostname) and optional port/path/query/fragment.
_URL_REGEX = re.compile(
    r"""
    ^(?P<scheme>https?)://                     # http or https scheme
    (?:                                       # optional userinfo
        (?P<userinfo>[^@/?#]+)@
    )?
    (?:                                       # host: IPv4, IPv6 or hostname
        \[(?P<ipv6>[0-9a-fA-F:.]+)\]          # IPv6 in brackets
        |
        (?P<ipv4>(?:\d{1,3}\.){3}\d{1,3})     # IPv4
        |
        (?P<hostname>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})  # hostname
    )
    (?::(?P<port>\d{1,5}))?                   # optional port
    (?:/(?P<path>[^\s?#]*))?                  # optional path
    (?:\?(?P<query>[^\s#]*))?                 # optional query
    (?:\#(?P<fragment>[^\s]*))?$              # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP/HTTPS URL,
    otherwise False. No exceptions are raised.

    The function uses a precompiled regular expression that avoids
    backtracking pitfalls and therefore is safe from CWE‑1333.
    """
    if not isinstance(link, str):
        return False
    match = _URL_REGEX.match(link)
    if not match:
        return False

    # Basic sanity checks on IPv4 octets
    ipv4 = match.group("ipv4")
    if ipv4:
        for part in ipv4.split("."):
            try:
                num = int(part)
            except ValueError:
                return False
            if not 0 <= num <= 255:
                return False

    # Validate port range if present
    port = match.group("port")
    if port:
        try:
            p = int(port)
        except ValueError:
            return False
        if not 0 <= p <= 65535:
            return False

    return True