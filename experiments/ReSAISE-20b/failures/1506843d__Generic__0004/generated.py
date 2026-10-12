#!/usr/bin/env python3
"""
SSRF safe URL inspector for external API endpoints.
"""

from __future__ import annotations

import ipaddress
import socket
import sys
from pathlib import Path
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: trusted domains (case‑insensitive)
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.api.partner.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """
    Determine if the supplied IP address is in a private or reserved range.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (likely a hostname)
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    Returns an empty list if resolution fails.
    """
    try:
        # Use getaddrinfo to support both IPv4 and IPv6
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

    addresses = []
    for info in infos:
        addr = info[4][0]
        addresses.append(addr)
    return addresses


def _is_hostname_trusted(hostname: str) -> bool:
    """
    Verify that the hostname matches one of the trusted domains.
    Subdomain matching is not allowed; only exact match.
    """
    hostname_lower = hostname.lower()
    return hostname_lower in TRUSTED_DOMAINS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The validated URL (unchanged).

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        points to a private/internal IP or hostname,
        or does not belong to the list of trusted domains.
    """
    # Parse URL
    parsed = urlparse(url_to_inspect)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url_to_inspect!r}")

    # Only allow http/https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed.scheme!r} in URL: {url_to_inspect}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Could not extract hostname from URL: {url_to_inspect}")

    # Reject localhost and loopback addresses
    if hostname.lower() in {"localhost", "127.0.0.1", "[::1]"}:
        raise ValueError(f"URL points to localhost: {url_to_inspect}")

    # Resolve hostname to IPs and check for private addresses
    resolved_ips = _resolve_hostname(hostname)
    if not resolved_ips:
        # If we cannot resolve, be conservative and reject
        raise ValueError(f"Could not resolve hostname {hostname!r} in URL: {url_to_inspect}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to a private IP {ip!r} in URL: {url_to_inspect}")

    # Check that the hostname is in the trusted list
    if not _is_hostname_trusted(hostname):
        raise ValueError(f"Hostname {hostname!r} is not in the list of trusted domains")

    # All checks passed; return the original URL
    return url_to_inspect


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://services.trusted.org/api/health",
        "https://malicious.com/data",          # should fail
        "http://127.0.0.1:8000/api",           # should fail
        "ftp://api.example.com/resource",      # should fail
    ]

    for u in test_urls:
        try:
            validated = inspect_api_url(u)
            print(f"✅ Validated: {validated}")
        except ValueError as e:
            print(f"❌ Invalid: {u} -> {e}", file=sys.stderr)