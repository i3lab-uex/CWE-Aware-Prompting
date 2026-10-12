#!/usr/bin/env python3
"""
validate_feed_url.py

Provides a single function `validate_feed_url` that ensures an RSS feed URL
originates from a pre‑approved external provider and does not point to an
internal or private network address.

This implementation mitigates SSRF (CWE‑918) by performing the following checks:
1. URL must use HTTP or HTTPS.
2. Hostname must be in a whitelist of trusted providers.
3. DNS resolution of the hostname must not resolve to any private or link‑local IP
   addresses (RFC1918, RFC1694, etc.).
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, unquote

# --------------------------------------------------------------------------- #
# Configuration: list of trusted RSS feed providers (hostnames or domain names)
# --------------------------------------------------------------------------- #
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
    # Add more trusted domains as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address string is private or otherwise disallowed.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    # Disallow private, loopback, link-local, multicast, and reserved addresses
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
    )


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the given hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    # getaddrinfo returns a list of (family, type, proto, canonname, sockaddr)
    addr_info = socket.getaddrinfo(hostname, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
    return [info[4][0] for info in addr_info]


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider and does
    not point to an internal or private network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all validation checks.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    originates from an untrusted provider, or resolves to
                    a private/internal IP address.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Hostname must be in the whitelist
    host = parsed.hostname.lower()
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname {host!r} is not in the list of trusted providers")

    # Resolve hostname to IP addresses
    try:
        ips = _resolve_hostname(host)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {host!r}: {exc}") from exc

    # Ensure none of the resolved IPs are private/internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip!r} for host {host!r} is private or disallowed")

    # All checks passed; return the original URL
    return url


# --------------------------------------------------------------------------- #
# Example usage (uncomment for quick test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost:8000/feed",  # Should raise ValueError
    ]

    for u in test_urls:
        try:
            print(f"Validating: {u}")
            validated = validate_feed_url(u)
            print("  --> Validated URL:", validated)
        except ValueError as e:
            print("  --> Validation error:", e)