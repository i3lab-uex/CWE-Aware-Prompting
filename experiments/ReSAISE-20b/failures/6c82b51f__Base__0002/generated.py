import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of trusted providers (domain names)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression for a valid URL scheme
URL_SCHEME_RE = re.compile(r"^(?:http|https)://", re.IGNORECASE)

# Private IP ranges to block (CWE-918 mitigation)
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fd00::/8"),   # Unique local addresses
    ipaddress.IPv6Network("fe80::/10")   # Link-local addresses
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False  # Not a valid IP
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False


def _normalize_url(rss_link: str) -> str:
    """Ensure the URL has a scheme and is percent‑encoded properly."""
    if not URL_SCHEME_RE.match(rss_link):
        raise ValueError("URL must start with http:// or https://")
    parsed = urlparse(rss_link)
    # Rebuild to enforce normalisation (e.g., remove fragments)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                       parsed.params, parsed.query, ""))


def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers
    and prevent Server‑Side Request Forgery (SSRF).

    Parameters:
        rss_link: str
            The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is malformed, not from a trusted provider,
                    or resolves to an internal/private IP address.
    """
    # Normalise URL
    url = _normalize_url(rss_link)

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against the whitelist
    if hostname.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Resolve the hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP ({ip})")

    # All checks passed; return the sanitized URL
    return url