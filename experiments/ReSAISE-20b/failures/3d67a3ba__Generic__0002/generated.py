import re

# Regular expression for a reasonably strict URL validation.
# This pattern covers:
#   - http, https, ftp, ftps schemes
#   - optional user:pass authentication
#   - IPv4 or IPv6 addresses
#   - domain names with TLDs
#   - optional port, path, query and fragment.
_URL_REGEX = re.compile(
    r"""
    ^(?P<scheme>https?|ftp|ftps)://                    # scheme
    (?:(?P<user>\w+)(?::(?P<pwd>[^@]*))?@)?            # optional user:pwd@
    (?:
        (?P<host>
            (?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)*   # subdomains
            [A-Za-z]{2,}                                     # TLD
        )
        |
        (?P<ipv4>
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|1?\d{1,2})){3}
        )
        |
        \[(?P<ipv6>[A-Fa-f0-9:]+)\]                      # IPv6
    )
    (?::(?P<port>\d{1,5}))?                            # optional port
    (?P<path>/[^?#\s]*)?                               # optional path
    (\?(?P<query>[^#\s]*))?                            # optional query
    (#(?P<fragment>\S*))?$                              # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Validate a URL string against a regular expression.

    Parameters
    ----------
    link : str
        The URL candidate to validate.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    try:
        return _URL_REGEX.match(link.strip()) is not None
    except Exception:
        # In case of unexpected input that could raise an exception,
        # we return False to satisfy the "no exceptions" requirement.
        return False