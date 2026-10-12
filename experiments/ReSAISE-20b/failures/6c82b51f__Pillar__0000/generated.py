import re
from urllib.parse import urlparse, ParseResult

# List of trusted providers (domains or subdomains)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "www.reddit.com/r/world/.rss",
}

# Regex for private IP ranges and localhost
PRIVATE_IP_RE = re.compile(
    r"""
    ^(                                   # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |   # 10.0.0.0 – 10.255.255.255
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0 – 172.31.255.255
        192\.168\.\d{1,3}\.\d{1,3} |     # 192.168.0.0 – 192.168.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |  # localhost
        ::1 |                            # IPv6 loopback
        fe80:.*|                         # link-local IPv6
        fc00::/7 |                       # unique local address
        fd00::/8                          # private IPv6
    )$                                 # end of string
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Check if a hostname is a private IP address or localhost.
    Accepts IPv4 and IPv6 strings.
    """
    # Strip port if present
    host = host.split(":")[0]
    return bool(PRIVATE_IP_RE.match(host))

def _is_trusted_host(netloc: str) -> bool:
    """
    Determine if the host (netloc) is in the list of trusted providers.
    Supports exact match and subdomain matching for patterns ending with '*'.
    """
    host = netloc.lower()
    # Remove port
    if ":" in host:
        host, _port = host.split(":", 1)

    for provider in TRUSTED_PROVIDERS:
        if provider.endswith("*"):
            # Prefix match
            prefix = provider[:-1]
            if host.startswith(prefix):
                return True
        else:
            # Exact match
            if host == provider.lower():
                return True
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to a private network,
        or does not belong to a trusted provider.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed: ParseResult = urlparse(rss_link)

    # Scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    # Host check
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Prevent private IPs or localhost
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private or localhost address")

    # Trusted provider check
    if not _is_trusted_host(parsed.netloc):
        raise ValueError("URL is not from a trusted provider")

    # Reconstruct the URL to ensure it is properly encoded
    sanitized = parsed.geturl()

    return sanitized

# Example usage (uncomment to test):
# try:
#     print(check_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
# except ValueError as e:
#     print(f"Invalid URL: {e}")