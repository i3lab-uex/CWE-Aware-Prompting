#!/usr/bin/env python3
"""
Utility to validate external webhook URLs before they are used internally.
"""

import re
import socket
from urllib.parse import urlparse, urlunparse

import ipaddress


# ----------------------------------------------------------------------
# Configuration: Whitelisted public API domains
# ----------------------------------------------------------------------
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.service.org",
    "trusted.partner.net",
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is a private or
    non‑routable address (RFC 1918, loopback, link local, etc.)."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
            ip
        ).is_loopback or ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host_to_ip(host: str) -> str:
    """Resolve a hostname to its first IPv4/IPv6 address.
    Raises socket.gaierror if resolution fails."""
    # Use getaddrinfo to support both IPv4 and IPv6
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    # Pick the first address
    return infos[0][4][0]


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it is used internally.

    Parameters
    ----------
    webhook_endpoint : str
        The external URL supplied by a third‑party system.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is safe for internal use.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist, or if it resolves to a private
        address (e.g., 10.x.x.x, 192.168.x.x, localhost, etc.).
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("webhook_endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are allowed")

    # Extract hostname; reject if missing
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize domain to lowercase for comparison
    host_lower = host.lower()

    # Check whitelist
    if host_lower not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Resolve hostname to IP and check for private addresses
    try:
        ip = _resolve_host_to_ip(host_lower)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve host '{host}': {exc}") from exc

    if _is_private_ip(ip):
        raise ValueError(
            f"Resolved IP '{ip}' for host '{host}' is private or non‑routable"
        )

    # Rebuild the URL to ensure no query/fragment manipulation
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{host}:{parsed.port}" if parsed.port else host,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url


# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://localhost:8000/hook",          # should fail
        "https://unknown.com/endpoint",       # should fail
        "http://webhooks.service.org:8080/callback",
    ]

    for url in test_urls:
        try:
            result = verify_webhook(url)
            print(f"✅ {url} -> {result}")
        except ValueError as e:
            print(f"❌ {url} -> {e}")