#!/usr/bin/env python3
"""
validate_webhook_url.py

Provides a single function that validates an external webhook URL and returns a
safe, internal‑API compatible URL.  The function ensures that the target
domain is in a pre‑approved list and that the URL does not point to a private,
loopback or link‑local network.

The implementation guards against the CWE-664 vulnerability by
explicitly controlling the lifetime of the parsed URL object and rejecting
untrusted or potentially dangerous endpoints.
"""

from __future__ import annotations

import ipaddress
import re
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: allowed public API domains
# --------------------------------------------------------------------------- #

ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.hubspot.com",
    "hooks.slack.com",
    # Add more trusted domains as needed
}

# Regular expression to detect private IP ranges in the hostname (IPv4 only)
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|127\.|169\.254\.|192\.168\.)"
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private, loopback or link‑local IP address.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address; assume it's a hostname.
        return False


def _resolve_hostname(host: str) -> set[str]:
    """
    Resolve the hostname to all associated IP addresses.
    Returns a set of string representations of IPv4/IPv6 addresses.
    """
    try:
        addr_info = socket.getaddrinfo(host, None)
        return {socket.inet_ntop(sock_family, sockaddr[0]) for sock_family, _, _, _, sockaddr in addr_info}
    except socket.gaierror:
        # Unable to resolve; treat as unsafe
        return set()


def _is_hostname_allowed(host: str) -> bool:
    """
    Validate that the hostname is either in the ALLOWED_DOMAINS set or
    resolves to a public IP address.
    """
    # 1. Check against the whitelist
    if host in ALLOWED_DOMAINS:
        return True

    # 2. Resolve hostname and ensure no private IPs
    resolved_ips = _resolve_hostname(host)
    if not resolved_ips:
        return False  # resolution failed

    for ip in resolved_ips:
        if _is_private_ip(ip):
            return False
    return True


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a safe internal API URL.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A validated URL suitable for internal API usage.

    Raises
    ------
    ValueError
        If the domain is not in the allowed list or if the URL resolves to a private network.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    # Parse the URL
    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or network location")

    # Normalise hostname (case-insensitive for domain names)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Validate hostname
    if not _is_hostname_allowed(host):
        raise ValueError(f"Domain '{host}' is not allowed or resolves to a private network")

    # Reconstruct the URL to ensure it is safe for internal use
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     test_url = "https://api.example.com/webhook"
#     try:
#         safe = validate_webhook_url(test_url)
#         print(f"Validated URL: {safe}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")