#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

This module provides a single function `secure_feed_link` that validates
an RSS feed URL against a list of trusted providers and ensures the target
cannot be an internal or private IP address.  The function is designed to
mitigate Server‑Side Request Forgery (CWE‑918) by preventing the server
from fetching content from untrusted or internal locations.

Author: OpenAI ChatGPT
"""

import re
import socket
from urllib.parse import urlparse, urlunparse


# --------------------------------------------------------------------------- #
# Configuration: list of trusted providers
# --------------------------------------------------------------------------- #
TRUSTED_PROVIDERS = {
    "news.example.com",
    "feeds.bbc.co.uk",
    "rss.cnn.com",
    "news.google.com",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """
    Determine if the given IP address is private or reserved.
    Supports IPv4 and IPv6.

    :param ip: String representation of an IP address
    :return: True if the IP is private/reserved, False otherwise
    """
    try:
        # socket.inet_aton works only for IPv4, so use ipaddress module
        import ipaddress

        address = ipaddress.ip_address(ip)
        return address.is_private or address.is_loopback or address.is_reserved
    except ValueError:
        # If parsing fails, treat as unsafe
        return True


def _resolve_hostname(hostname: str) -> set[str]:
    """
    Resolve a hostname to all associated IP addresses.

    :param hostname: Hostname to resolve
    :return: Set of stringified IP addresses
    """
    try:
        # getaddrinfo returns a list of tuples; we extract the IP part
        infos = socket.getaddrinfo(hostname, None)
        return {info[4][0] for info in infos}
    except socket.gaierror:
        # Hostname could not be resolved
        return set()


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    The function checks that the URL uses HTTPS, points to a trusted
    provider, and resolves to at least one public IP address.  It also
    normalizes the URL by removing fragments and query parameters that
    are not relevant to the feed content.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a non‑HTTPS scheme,
        points to an untrusted provider, or resolves to a private
        or reserved IP address.
    """
    if not isinstance(rss_url, str):
        raise ValueError("RSS URL must be a string")

    parsed = urlparse(rss_url)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Host must be in the trusted providers list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Normalize hostname to lowercase for comparison
    hostname_lower = hostname.lower()
    if hostname_lower not in TRUSTED_PROVIDERS:
        raise ValueError(f"Host '{hostname}' is not a trusted provider")

    # 3. Resolve hostname and ensure at least one public IP
    resolved_ips = _resolve_hostname(hostname_lower)
    if not resolved_ips:
        raise ValueError(f"Unable to resolve host '{hostname}'")

    # Verify that none of the resolved IPs are private or reserved
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for host '{hostname}' is private or reserved"
            )

    # 4. Rebuild the URL without fragments and query parameters
    sanitized = parsed._replace(fragment="", query="")

    # Return the canonicalized URL
    return urlunparse(sanitized)


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://news.example.com/rss/latest",
        "http://malicious.com/feed",  # Should fail
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            safe_url = secure_feed_link(url)
            print(f"  → Sanitized URL: {safe_url}\n")
        except ValueError as exc:
            print(f"  → Validation error: {exc}\n")