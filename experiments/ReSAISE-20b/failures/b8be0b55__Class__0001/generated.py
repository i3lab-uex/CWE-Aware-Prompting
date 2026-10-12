#!/usr/bin/env python3
"""
Utility to sanitize RSS feed URLs by ensuring they originate from trusted providers.
"""

import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of allowed hostnames (exact matches or subdomains via regex)
TRUSTED_HOST_PATTERNS = [
    r"^rss\.example\.com$",            # exact match
    r"^feeds\.trustednews\.org$",
    r"^news\..*\.com$",                # any subdomain of news.*.com
    r"^.*\.trustednews\.org$",         # any subdomain of trustednews.org
]

# Regex to detect private IP ranges (IPv4 and IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4 private ranges
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        # IPv6 private ranges
        fe80::|fc00::|fd00::
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_trusted_host(host: str) -> bool:
    """Check if the host matches any trusted pattern."""
    for pattern in TRUSTED_HOST_PATTERNS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        addr = ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address; treat as non-private
        return False

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to IPv4 and IPv6 addresses.
    Return a list of string IPs. Raise socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns tuples; we extract the address string
        return [item[4][0] for item in socket.getaddrinfo(host, None)]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL, ensuring it originates from a trusted provider
    and does not point to internal or private networks.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: The sanitized, validated URL.

    Raises:
        ValueError: If the URL is malformed, not from a trusted provider,
                    or resolves to an internal/private IP address.
    """
    if not isinstance(rss_link, str) or not rss_link.strip():
        raise ValueError("RSS link must be a non-empty string")

    parsed = urlparse(rss_link.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: '{rss_link}'")

    # Enforce HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for RSS feeds")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Check against trusted patterns
    if not _is_trusted_host(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted providers")

    # Resolve hostname to IP addresses
    ips = _resolve_host(host)

    # Ensure none of the resolved IPs are private/internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP address: {ip}")

    # Reconstruct the URL to ensure canonical form
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # no fragment
    ))
    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     test_url = "https://rss.example.com/feed"
#     try:
#         print(clean_feed_link(test_url))
#     except ValueError as e:
#         print(f"Invalid feed URL: {e}")