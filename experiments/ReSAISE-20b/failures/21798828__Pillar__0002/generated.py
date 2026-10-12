#!/usr/bin/env python3
"""
Utility to safely validate webhook URLs that point to approved internal API endpoints.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration – list of approved API endpoints
# Each entry can be a hostname or an IP address (IPv4/IPv6).
# The scheme must be http or https.
#
# Example:
#   approved_endpoints = {"api.example.com", "127.0.0.1"}
# --------------------------------------------------------------------------- #
approved_endpoints = {
    "api.internal.example.com",
    "127.0.0.1",          # localhost
    "::1",                # IPv6 localhost
    "10.0.0.1",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_internal_ip(ip: str) -> bool:
    """
    Determine if an IP address is within private or loopback ranges.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_reserved  # e.g., 0.0.0.0, 255.255.255.255
        or addr.is_multicast
    )


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IP addresses.
    Returns an empty list if resolution fails.
    """
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except (socket.gaierror, UnicodeError):
        return []


def _is_approved(hostname: str) -> bool:
    """
    Verify that the hostname is in the approved list or resolves to an
    approved IP address.
    """
    # Direct match on hostname
    if hostname in approved_endpoints:
        return True

    # Resolve the hostname to IPs and check each
    for ip in _resolve_hostname(hostname):
        if ip in approved_endpoints:
            return True
        # If the IP itself is private/loopback, reject it
        if _is_internal_ip(ip):
            return False

    # No approved match found
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL that points to an approved internal API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by the external service.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to an internal network location.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Scheme validation
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Hostname validation
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal IPs directly in the URL
    try:
        ipaddress.ip_address(hostname)
        if _is_internal_ip(hostname):
            raise ValueError(f"URL points to an internal IP address: {hostname}")
    except ValueError:
        # Not a raw IP – it's a hostname; check against approved list
        if not _is_approved(hostname):
            raise ValueError(f"Hostname {hostname!r} is not an approved endpoint")

    # Reconstruct the URL to ensure it is normalized
    sanitized = urlunparse((
        parsed.scheme,
        f"{hostname}:{parsed.port}" if parsed.port else hostname,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.internal.example.com/v1/notify",
        "http://127.0.0.1:8000/callback",
        "https://malicious.com/evil",
    ]

    for url in test_urls:
        try:
            result = handle_webhook(url)
            print(f"✅ {url} -> {result}")
        except ValueError as e:
            print(f"❌ {url} : {e}")