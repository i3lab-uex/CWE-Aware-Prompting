#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

This module provides the `secure_feed_link` function which checks that a
supplied RSS feed URL resolves to one of the trusted providers and does not
point to any internal or private IP address ranges.  It mitigates SSRF attacks
by performing a thorough host resolution and IP validation before allowing
the URL to be used.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import socket
import urllib.parse
from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network

# --------------------------------------------------------------------------- #
# Trusted provider hostnames and their allowed IP ranges
# --------------------------------------------------------------------------- #

TRUSTED_PROVIDERS = {
    # Example providers; add your own trusted domains here
    "rss.nytimes.com": {"ip_network('104.244.42.0/24')"},
    "feeds.feedburner.com": {"ip_network('216.239.38.0/24')"},
    "blog.feedly.com": {"ip_network('34.68.195.0/24')"},
}

# Internal / private IP networks that must be blocked
PRIVATE_NETWORKS = {
    ip_network("0.0.0.0/8"),
    ip_network("10.0.0.0/8"),
    ip_network("127.0.0.0/8"),
    ip_network("169.254.0.0/16"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("224.0.0.0/4"),   # Multicast
    ip_network("240.0.0.0/5"),   # Reserved for future use
    ip_network("255.255.255.255/32"),
    # IPv6 equivalents
    ip_network("::1/128"),   # Loopback
    ip_network("fc00::/7"),  # Unique local addresses
    ip_network("fe80::/10")  # Link-local unicast
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_ip_allowed(ip: IPv4Address | IPv6Address) -> bool:
    """
    Check if the given IP address is not part of any private network.
    """
    for net in PRIVATE_NETWORKS:
        if ip in net:
            return False
    return True

def _is_trusted_host(host: str) -> bool:
    """
    Validate that the host is among the trusted providers.
    """
    return host.lower() in TRUSTED_PROVIDERS

def _resolve_host(host: str) -> list[IPv4Address | IPv6Address]:
    """
    Resolve the host to all its IP addresses (both IPv4 and IPv6).
    Raises socket.gaierror if resolution fails.
    """
    addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    ips = []
    for info in addrinfo:
        ip_str = info[4][0]
        try:
            ips.append(ip_address(ip_str))
        except ValueError:
            continue  # skip malformed addresses
    return ips

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL supplied by an untrusted source.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, does not resolve to a trusted host,
        or resolves to an IP address within a private network.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(rss_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {rss_url}")

    # Normalise host (case-insensitive for domain names)
    host = parsed.hostname
    if not host:
        raise ValueError(f"URL missing hostname: {rss_url}")

    # 1. Verify host is in the trusted list
    if not _is_trusted_host(host):
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # 2. Resolve host to IP addresses
    try:
        resolved_ips = _resolve_host(host)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve host '{host}': {exc}") from exc

    if not resolved_ips:
        raise ValueError(f"Host '{host}' did not resolve to any IP addresses")

    # 3. Ensure none of the resolved IPs are private
    for ip in resolved_ips:
        if not _is_ip_allowed(ip):
            raise ValueError(
                f"Resolved IP {ip} for host '{host}' is in a private network"
            )

    # 4. Reconstruct the URL to ensure no hidden malicious query parameters
    sanitized = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            "",  # Remove params
            "",  # Remove query
            ""   # Remove fragment
        )
    )

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test with a known trusted provider
    try:
        url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        safe_url = secure_feed_link(url)
        print(f"Validated URL: {safe_url}")
    except ValueError as e:
        print(f"Validation failed: {e}")