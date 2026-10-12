import re

# Regular expression for a reasonably strict URL validation.
# It matches http/https URLs with optional www, domain name or IP,
# optional port, path, query and fragment.
_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://                                   # http or https scheme
    (?:(?P<user>\w+)(?::(?P<pwd>[^@]+))?@)?                 # optional user:pass@
    (?:
        \[?(?P<ipv6>[A-Fa-f0-9:]+)\]?(?:\.(?P<ipv6>[A-Fa-f0-9:]+))*   # IPv6 address
        |                                                   # or
        (?P<ipv4>(?:\d{1,3}\.){3}\d{1,3})                    # IPv4 address
        |                                                   # or
        (?P<domain>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})        # domain name
    )
    (?::(?P<port>\d{1,5}))?                                 # optional port
    (?P<path>/[^\s?#]*)?                                     # optional path
    (?:\?(?P<query>[^\s#]*))?                                # optional query
    (?:\#(?P<fragment>[^\s]*))?$                             # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Verify whether the given string is a valid URL.

    Parameters
    ----------
    link : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if the URL matches the pattern, False otherwise.
    """
    # Ensure we work with a string; if not, return False
    if not isinstance(link, str):
        return False

    # Strip leading/trailing whitespace to avoid accidental mismatches
    link = link.strip()

    # If the string is empty after stripping, it's not a valid URL
    if not link:
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    try:
        return _URL_RE.fullmatch(link) is not None
    except re.error:
        # In the unlikely event of a regex error, treat as invalid
        return False