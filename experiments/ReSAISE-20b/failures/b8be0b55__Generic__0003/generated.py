import re
import socket
from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# A list of trusted RSS feed providers.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",          # Google News
    "rss.cnn.com",
    "feeds.reuters.com",
    "www.bbc.co.uk",           # BBC main
}

# Regular expression to detect private IP address ranges.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP string is a private or loopback address.
    """
    try:
        addr = ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address.
        return False

def _hostname_resolves_to_private(hostname: str) -> bool:
    """
    Resolve the hostname and return True if any of its addresses are private.
    """
    try:
        for result in socket.getaddrinfo(hostname, None):
            family, _, _, _, sockaddr = result
            if family in (socket.AF_INET, socket.AF_INET6):
                ip = sockaddr[0]
                if _is_private_ip(ip):
                    return True
    except socket.gaierror:
        # DNS resolution failed; treat as unsafe.
        return True
    return False

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL by ensuring it originates from a trusted provider
    and does not point to any internal or private network address.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, untrusted, or resolves to a private address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Basic validation: scheme and netloc must be present
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Check for internal IPs directly in the hostname
    if PRIVATE_IP_REGEX.match(parsed.netloc):
        raise ValueError("URL points to a private IP address")

    # Resolve hostname and ensure no private addresses
    if _hostname_resolves_to_private(parsed.hostname):
        raise ValueError("URL resolves to a private IP address")

    # Ensure hostname is in the trusted list
    if parsed.hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not a trusted provider")

    # All checks passed
    return rss_link