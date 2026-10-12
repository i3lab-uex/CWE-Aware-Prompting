import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully-qualified domain names that are considered trusted providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "feed.theguardian.com",
    # Add more providers as needed
}

# Regular expression to match common private IP address ranges.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                 # start of string
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |           # 10.0.0.0/8
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |  # 172.16.0.0/12
        (?:192\.168\.\d{1,3}\.\d{1,3}) |                # 192.168.0.0/16
        (?:169\.254\.\d{1,3}\.\d{1,3}) |                # 169.254.0.0/16
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3}) |            # 127.0.0.0/8
        (?:::1)                                         # IPv6 loopback
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    Handles both IPv4 and IPv6 literal addresses.
    """
    try:
        # Directly check if host is a literal IP address
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a literal IP; use regex to catch common private patterns
        return bool(PRIVATE_IP_REGEX.match(host))

def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be sanitized.

    Returns
    -------
    str
        A cleaned, fully-qualified URL that is known to come from a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal/private network,
        or does not belong to a trusted provider.
    """
    if not isinstance(rss_link, str) or not rss_link.strip():
        raise ValueError("rss_link must be a non-empty string")

    parsed = urlparse(rss_link.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("rss_link must be a valid absolute URL")

    # Reject URLs that point to private IP addresses or local hostnames
    hostname = parsed.hostname.lower()
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private or internal IP address")

    # Verify that the host is in our trusted provider list
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {hostname}")

    # Reconstruct the URL to ensure no extraneous fragments or queries
    cleaned = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return cleaned