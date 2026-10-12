#!/usr/bin/env python3
"""
Utility to validate RSS feed URLs against a whitelist of trusted providers.
The function raises ValueError if the URL points to an untrusted domain
or resolves to a private/internal IP address.
"""

from __future__ import annotations

import re
import socket
import sys
import ipaddress
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted providers (add or remove domains as needed)
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to extract the hostname from a URL
HOSTNAME_RE = re.compile(r"^[^@]+@([^:]+)", re.IGNORECASE)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string belongs to a private or
    loopback network as defined by RFC 1918, RFC 4193, and RFC 5735.
    """
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Invalid IP address string
        return False

def _hostname_resolves_to_private(hostname: str) -> bool:
    """
    Resolve the hostname to all IP addresses and check if any are private.
    If any address is private, return True.
    """
    try:
        # Get all addresses for the hostname
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # DNS resolution failed; treat as unsafe
        return True

    for family, _, _, _, sockaddr in infos:
        # sockaddr can be a tuple like (ip, port) or ((ipv6, ...), ...)
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return True
    return False

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def clean_feed_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The URL to validate.

    Returns
    -------
    str
        The original RSS link if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL does not use http/https, resolves to an internal IP,
        or its hostname is not in the trusted list.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize hostname (lowercase)
    hostname = hostname.lower()

    # Reject if hostname is not in the whitelist
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Resolve hostname and ensure it does not map to an internal IP
    if _hostname_resolves_to_private(hostname):
        raise ValueError(f"Hostname '{hostname}' resolves to a private IP address")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.feedburner.com/somefeed",
        "https://localhost/feed.xml",  # should raise ValueError
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            clean = clean_feed_link(url)
            print(f"  -> Sanitized URL: {clean}")
        except ValueError as e:
            print(f"  ERROR: {e}", file=sys.stderr)