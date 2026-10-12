import re
from urllib.parse import urlparse
import socket
import ipaddress

# List of trusted RSS providers (add as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    # Add more trusted domains here
}

# Regex to detect private IP address ranges (IPv4 and IPv6)
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        # IPv4 private ranges
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (192\.168\.\d{1,3}\.\d{1,3})|
        # IPv6 private ranges
        (fc00::/7)|
        (fe80::/10)
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _hostname_to_ip(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and
    does not resolve to an internal or private network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is trusted and safe.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP,
                    not from a trusted domain, or resolves to
                    an internal/private IP address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Check against the list of trusted domains
    if hostname.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _hostname_to_ip(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address ({ip})")

    return source_url