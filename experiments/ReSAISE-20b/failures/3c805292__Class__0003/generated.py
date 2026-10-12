import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of trusted providers (domains or domain patterns)
TRUSTED_PROVIDERS = [
    r"^rss\.cnn\.com$",
    r"^feeds\.bbc\.co\.uk$",
    r"^news\.nytimes\.com$",
    r"^.*\.guardian\.co\.uk$",  # allow subdomains
]

# Regular expression to detect private IP address ranges (CWE‑441 prevention)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),      # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),     # Unique local address (ULA)
]


def _is_private_ip(hostname: str) -> bool:
    """Return True if the hostname resolves to a private IP address."""
    try:
        # Resolve all addresses (IPv4 and IPv6)
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False  # cannot resolve; treat as public

    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue  # skip invalid
        for net in PRIVATE_IP_RANGES:
            if ip_obj in net:
                return True
    return False


def _is_trusted_provider(hostname: str) -> bool:
    """Check if the hostname matches one of the trusted provider patterns."""
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, hostname.lower()):
            return True
    return False


def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to connect to a private network.
    """
    # Basic URL parsing
    parsed = urlparse(feed_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {feed_address}")

    # Force https for safety
    scheme = "https"

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Could not determine host from URL: {feed_address}")

    # Reject private IPs or internal hosts
    if _is_private_ip(hostname):
        raise ValueError(f"URL resolves to a private IP address: {feed_address}")

    # Reject non-trusted providers
    if not _is_trusted_provider(hostname):
        raise ValueError(f"Host '{hostname}' is not a trusted provider.")

    # Reconstruct the URL with the enforced scheme
    sanitized = urlunparse(
        (
            scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized