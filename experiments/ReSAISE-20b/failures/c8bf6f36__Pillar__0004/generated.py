#!/usr/bin/env python3
"""
validate_rss_link.py

Provides a single function, `validate_rss_link`, which ensures that
a given RSS feed URL comes from a trusted external provider.  The
function checks the scheme, the host domain against an approved list,
and rejects URLs that resolve to private or loopback IP addresses
to guard against accidental internal network access.

The implementation follows defensive programming principles and
addresses CWE‑664 (Improper Control of a Resource Through its Lifetime)
by strictly validating the resource URL before any further use.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: Trusted providers
# --------------------------------------------------------------------------- #

_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
    # Add more trusted domains as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Invalid IP address; treat as unsafe.
        return True


def _resolve_host_to_ip(host: str) -> list[str]:
    """
    Resolve a hostname to its IPv4 and IPv6 addresses.
    Returns an empty list if resolution fails.
    """
    try:
        infos = socket.getaddrinfo(host, None)
        return [info[4][0] for info in infos]
    except socket.gaierror:
        return []


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL, ensuring it originates from a trusted provider
    and does not point to private or internal networks.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to a trusted
        external provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        references a non‑trusted domain, or resolves to a private IP address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link.strip())

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host check
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise the host to lowercase for comparison
    host_lower = host.lower()

    if host_lower not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted provider: {host}")

    # Resolve host to IP(s) and ensure none are private or loopback
    ips = _resolve_host_to_ip(host)
    if not ips:
        raise ValueError(f"Unable to resolve host: {host}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Host resolves to a private IP: {ip}")

    # Reconstruct the URL in a canonical form
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            host_lower,
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query if any
            "",  # fragment
        )
    )

    return sanitized


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "https://malicious.example.com/feed.xml",  # should raise
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_rss_link(url)
            print(f"  -> Validated URL: {result}\n")
        except ValueError as exc:
            print(f"  -> Validation failed: {exc}\n")