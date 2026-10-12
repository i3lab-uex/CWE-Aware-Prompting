import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Trusted RSS providers (add or remove domains as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",          # example
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression for private IP ranges
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.|127\.0\.0\.1|
    ::1|fc00:|fd00:)  # IPv6 private ranges
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _validate_hostname(hostname: str) -> bool:
    """Check that the hostname resolves to a public IP and is trusted."""
    # Resolve all addresses for the host
    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return False
    # Check domain trust
    for trusted in _TRUSTED_DOMAINS:
        if hostname.lower().endswith(trusted):
            return True
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider
    and does not resolve to a private or internal network address.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not trusted or attempts to access a restricted network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Basic URL checks
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL missing network location (hostname)")

    # Resolve hostname to IPs and ensure they are public
    if not _validate_hostname(parsed.hostname):
        raise ValueError("Hostname is not from a trusted provider or resolves to a private IP")

    # Reconstruct the URL to ensure it's clean
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized