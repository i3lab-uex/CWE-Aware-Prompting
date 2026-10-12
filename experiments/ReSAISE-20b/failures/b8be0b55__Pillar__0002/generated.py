import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "feeds.reuters.com",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.bbci.co.uk",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        10\.                       # 10.0.0.0/8
      | 172\.(?:1[6-9]|2\d|3[0-1])\.  # 172.16.0.0/12
      | 192\.168\.                  # 192.168.0.0/16
      | 127\.\d{1,3}\.\d{1,3}\.\d{1,3}  # localhost
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given string is a private IP address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _normalize_url(url: str) -> str:
    """
    Normalize the URL to a standard form (lowercase scheme and netloc, no default ports).
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    return urlunparse((scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))

def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL supplied by a user or external source.

    Returns
    -------
    str
        The sanitized, validated URL that is guaranteed to originate from a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, points to a private IP address,
        or does not belong to one of the trusted domains.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that explicitly contain private IP addresses
    host = parsed.hostname or ""
    if PRIVATE_IP_REGEX.match(host) or _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Ensure the domain is in the trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Return a canonical form of the URL
    return _normalize_url(rss_link)