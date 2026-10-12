#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

This module provides a single function, `secure_feed_link`, which validates an
RSS feed URL against a whitelist of trusted providers and ensures that the URL
does not resolve to any private or internal IP address.  The function raises a
`ValueError` if the URL is not trusted or attempts to reach an internal network.
"""

import re
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: Trusted providers and private IP ranges
# --------------------------------------------------------------------------- #

# Example whitelist of trusted feed hosts (case‑insensitive)
TRUSTED_HOSTS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regular expression to detect IPv4 addresses in the URL (if present)
IPV4_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")

# Private IP ranges (RFC1918 + loopback)
PRIVATE_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),  # Loopback
    ("169.254.0.0", "169.254.255.255"),  # Link‑local
]

def _ip_to_int(ip: str) -> int:
    """Convert dotted IPv4 string to a 32‑bit integer."""
    parts = [int(p) for p in ip.split(".")]
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

def _ip_in_private_range(ip: str) -> bool:
    """Return True if the IP is within any of the private ranges."""
    ip_int = _ip_to_int(ip)
    for start, end in PRIVATE_RANGES:
        if _ip_to_int(start) <= ip_int <= _ip_to_int(end):
            return True
    return False

def _resolve_host(host: str) -> list[str]:
    """Return a list of resolved IPv4 addresses for the host."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror:
        # Host could not be resolved; treat as unsafe
        return []

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate and sanitize.

    Returns
    -------
    str
        The sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, uses an unsafe scheme,
        or resolves to a private/internal IP address.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    # Parse the URL
    parsed = urlparse(rss_url)

    # Ensure scheme is http or https (no ftp, file, etc.)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host; strip port if present
    netloc = parsed.hostname
    if not netloc:
        raise ValueError("URL must contain a hostname")

    # Normalize host to lowercase
    netloc = netloc.lower()

    # Reject if hostname is an IP address in private ranges
    if IPV4_RE.match(netloc):
        if _ip_in_private_range(netloc):
            raise ValueError(f"URL resolves to a private IP: {netloc}")
        # If it's a public IP, still reject unless we explicitly allow it
        raise ValueError(f"Public IP addresses are not allowed: {netloc}")

    # Check against trusted host whitelist
    if netloc not in TRUSTED_HOSTS:
        raise ValueError(f"Hostname '{netloc}' is not a trusted provider")

    # Resolve the host to ensure it does not point to an internal IP
    resolved_ips = _resolve_host(netloc)
    if not resolved_ips:
        raise ValueError(f"Could not resolve hostname: {netloc}")

    for ip in resolved_ips:
        if _ip_in_private_range(ip):
            raise ValueError(
                f"Hostname '{netloc}' resolves to private IP {ip}"
            )

    # Reconstruct the URL to ensure it is canonical
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         url = secure_feed_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")