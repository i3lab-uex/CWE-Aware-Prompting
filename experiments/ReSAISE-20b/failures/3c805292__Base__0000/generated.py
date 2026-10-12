#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

The function ensures that only URLs pointing to trusted public providers are allowed,
preventing Server‑Side Request Forgery (CWE‑918) and internal network access.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# A whitelist of trusted providers (domain suffixes or full hostnames).
TRUSTED_PROVIDERS = {
    # Example providers – replace with real trusted domains.
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.reuters.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_private_ip(host: str) -> bool:
    """
    Resolve host to IP addresses and check if any are private or loopback.
    """
    try:
        # Resolve all IP addresses for the hostname
        ips = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        # If hostname cannot be resolved, treat it as invalid
        return True

    for _, _, _, _, sockaddr in ips:
        ip = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
        except ValueError:
            continue
    return False


def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The raw URL supplied by an upstream component.

    Returns
    -------
    str
        A sanitized, validated URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/loopback IP, or does not match the trusted provider list.
    """
    # Basic parsing
    parsed = urlparse(feed_address.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Enforce allowed schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that resolve to private IPs or localhost
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or loopback address")

    # Ensure the hostname matches one of the trusted providers
    host = parsed.hostname.lower()
    if not any(host == provider or host.endswith("." + provider) for provider in TRUSTED_PROVIDERS):
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Re‑build the URL to ensure canonical form
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return sanitized


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "http://localhost/feed",
        "ftp://example.com/resource",
        "https://malicious.site/steal",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_feed_source(url)
            print("  -> Valid:", result)
        except ValueError as exc:
            print(f"  -> Invalid: {exc}")