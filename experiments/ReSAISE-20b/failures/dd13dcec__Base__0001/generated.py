#!/usr/bin/env python3
"""
sanitize_feed_url: Validate RSS feed URLs against a whitelist and prevent SSRF.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.parse
from typing import Iterable, List


# --- Trusted providers ----------------------------------------------------
TRUSTED_DOMAINS: List[str] = [
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    # Add more trusted providers here
]


# --- Private / restricted IP ranges ---------------------------------------
PRIVATE_IP_RANGES: Iterable[ipaddress._BaseNetwork] = (
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),   # Unique local address
)


def _is_ip_private(ip: str) -> bool:
    """
    Return True if the IP address is in a private or restricted range.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # Invalid IP address
        return True

    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False


def _resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve the hostname to a list of IP addresses.
    Raise socket.gaierror if resolution fails.
    """
    # We only want IPv4 and IPv6 addresses
    return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that `feed_url` points to a trusted RSS provider and does not
    resolve to any internal or restricted IP address.

    Parameters:
        feed_url (str): The URL supplied by the user.

    Returns:
        str: The sanitized, validated URL (unchanged if valid).

    Raises:
        ValueError: If the URL is not from a trusted provider or resolves
                    to an internal / restricted IP.
    """
    if not feed_url:
        raise ValueError("feed_url must be a non-empty string")

    # Parse the URL and validate scheme
    parsed = urllib.parse.urlparse(feed_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the hostname for case-insensitive comparison
    hostname_lower = hostname.lower()

    if hostname_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Resolve the hostname and ensure no IP resolves to private ranges
    try:
        ips = _resolve_hostname(hostname_lower)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve hostname '{hostname}': {exc}") from exc

    for ip in ips:
        if _is_ip_private(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to restricted IP address {ip}"
            )

    # All checks passed; return the original URL unchanged
    return feed_url