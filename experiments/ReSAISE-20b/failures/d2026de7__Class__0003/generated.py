import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved RSS providers (example list)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com"
}

# Private IP networks to block
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8")
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in net for net in PRIVATE_NETWORKS)
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL points to a trusted provider and does not
    resolve to private or internal IP addresses.

    Args:
        rss_address: The RSS feed URL to validate.

    Returns:
        A sanitized RSS feed URL that is guaranteed to point to a trusted provider.

    Raises:
        ValueError: If the URL is not from an approved provider or attempts to
                    access restricted internal networks.
    """
    if not isinstance(rss_address, str):
        raise ValueError("rss_address must be a string")

    # Basic URL parsing
    parsed = urlparse(rss_address)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalise hostname (lowercase)
    hostname = hostname.lower()

    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not an approved provider")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to private IP {ip}, which is not allowed"
            )

    # Reconstruct the URL to ensure it has a standard format
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized