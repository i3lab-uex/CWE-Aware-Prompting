#!/usr/bin/env python3
"""
validate_feed_source.py

Secure RSS feed URL validation to prevent SSRF attacks.
"""

from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of trusted providers (case‑insensitive). Expand as needed.
_TRUSTED_PROVIDERS = {
    "feedly.com",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.bbci.co.uk",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_ip_private(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or link‑local."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host(hostname: str) -> list[str]:
    """Resolve a hostname to a list of IP addresses."""
    try:
        return [r[4][0] for r in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider
    and does not resolve to a private or restricted network address.

    Parameters:
        feed_address (str): The URL to validate.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not trusted or resolves to a restricted network.
    """
    # Parse and normalise
    parsed = urlparse(feed_address)
    scheme = parsed.scheme.lower()
    netloc = parsed.hostname
    if not scheme or scheme not in _ALLOWED_SCHEMES:
        raise ValueError("URL must use http or https scheme")

    if not netloc:
        raise ValueError("URL does not contain a valid hostname")

    # Check against trusted providers
    if netloc.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{netloc}' is not in the list of trusted providers")

    # Resolve hostname and ensure no IP resolves to a restricted network
    ips = _resolve_host(netloc)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{netloc}'")

    for ip in ips:
        if _is_ip_private(ip):
            raise ValueError(
                f"Resolved IP {ip} for hostname '{netloc}' is in a private or restricted network"
            )

    # Reconstruct the URL to ensure it has no query or fragment
    sanitized = urlunparse(
        (
            scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )
    return sanitized


# Example usage (for manual testing only)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost/feed.xml",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_feed_source(url)
            print(" -> Validated URL:", result)
        except ValueError as e:
            print(" -> Validation failed:", e)