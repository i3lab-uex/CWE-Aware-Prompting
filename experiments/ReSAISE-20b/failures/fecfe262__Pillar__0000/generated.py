#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

This module provides a single function, `filter_rss_feed`, which checks that
an RSS feed URL originates from an approved public provider and does not
attempt to resolve to a private, loopback or link‑local address.  The function
returns the original URL unchanged if it passes all checks, otherwise a
`ValueError` is raised.

The implementation follows best practices for URL validation and DNS
resolution, guarding against common pitfalls such as host header injection,
IP address spoofing, and internal network access.
"""

from __future__ import annotations

import ipaddress
import socket
import ssl
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration – trusted providers
# --------------------------------------------------------------------------- #

TRUSTED_DOMAINS = {
    # News outlets
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "feeds.theguardian.com",
    # Tech blogs
    "rss.techcrunch.com",
    # Other public RSS providers
    "rss.cnn.com",
}

# Allow subdomains of the trusted domains (e.g. `blog.example.com`).
def is_trusted_host(host: str) -> bool:
    host = host.lower()
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _resolve_host_to_ips(host: str) -> list[ipaddress._BaseAddress]:
    """Resolve a hostname to all its IPv4/IPv6 addresses.

    The function uses `socket.getaddrinfo` which follows system DNS
    configuration, including local overrides.  It returns a list of
    `ipaddress` objects.
    """
    try:
        # Resolve host to all address families (AF_INET and AF_INET6)
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    ips = []
    for family, _, _, _, sockaddr in addrinfo:
        ip_str = sockaddr[0]
        try:
            ips.append(ipaddress.ip_address(ip_str))
        except ValueError:
            # Skip invalid IPs (should not happen)
            continue
    return ips

def _is_ip_allowed(ip: ipaddress._BaseAddress) -> bool:
    """Return True if the IP is public and routable."""
    # Exclude private, loopback, link-local, documentation, and reserved addresses
    if ip.is_private or ip.is_loopback or ip.is_link_local:
        return False
    # Exclude IPv4 addresses that are reserved for documentation (e.g., 192.0.2.0/24)
    if ip.is_reserved or ip.is_multicast:
        return False
    return True

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate an RSS feed URL against a list of trusted providers and ensure it
    does not resolve to any internal or private network addresses.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP, not from a trusted
                    provider, or resolves to an internal/private IP.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url)

    # Basic scheme check
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Host must be in the trusted list
    if not is_trusted_host(host):
        raise ValueError(f"Hostname '{host}' is not an approved RSS provider")

    # Resolve the hostname to IP addresses and verify each
    for ip in _resolve_host_to_ips(host):
        if not _is_ip_allowed(ip):
            raise ValueError(f"Hostname '{host}' resolves to restricted IP address {ip}")

    # Reconstruct a canonical URL (ensure path is present)
    # Remove default ports for http/https
    netloc = host
    if parsed.port:
        # Only include the port if it differs from default
        if (parsed.scheme == "http" and parsed.port != 80) or \
           (parsed.scheme == "https" and parsed.port != 443):
            netloc += f":{parsed.port}"

    sanitized = urlunparse((
        parsed.scheme.lower(),
        netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.feedburner.com/TechCrunch/",
        "https://example.internal/feed.xml",  # should raise ValueError
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            clean = filter_rss_feed(url)
            print(f"  -> Accepted: {clean}\n")
        except ValueError as exc:
            print(f"  -> Rejected: {exc}\n")