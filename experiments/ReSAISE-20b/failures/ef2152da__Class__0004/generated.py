#!/usr/bin/env python3
"""
Utility to validate an external webhook callback URL before it is used internally.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration:  whitelist of approved domains
WHITELIST_DOMAINS = {
    "api.example.com",
    "webhook.partner.org",
    # Add more domains as needed
}

# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback or reserved range.
    """
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


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    Raises socket.gaierror if the name cannot be resolved.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
        return [sock[4][0] for sock in infos]
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc


def validate_callback(callback_url: str) -> str:
    """
    Validate that a callback URL is safe to be used internally.

    Parameters
    ----------
    callback_url : str
        The external webhook URL supplied by a third‑party service.

    Returns
    -------
    str
        The validated URL (unchanged) if it passes all checks.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTPS, the domain is not whitelisted,
        or the resolved IP addresses are private/internal.
    """
    if not callback_url:
        raise ValueError("callback_url must be a non-empty string")

    parsed = urlparse(callback_url)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only 'https' URLs are allowed for callbacks")

    # 2. Domain must be in the whitelist
    domain = parsed.hostname
    if not domain:
        raise ValueError("URL must contain a valid hostname")

    # Normalize to lowercase for comparison
    domain_lower = domain.lower()
    if domain_lower not in WHITELIST_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not in the approved whitelist")

    # 3. Resolve hostname and ensure no private IPs are reachable
    ip_addresses = _resolve_hostname(domain_lower)
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for domain '{domain}' is a private/internal address"
            )

    # 4. Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed)

    return safe_url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test cases
    test_urls = [
        "https://api.example.com/webhook",
        "http://api.example.com/webhook",  # Should fail: HTTP
        "https://malicious.example.net/evil",
    ]

    for url in test_urls:
        try:
            result = validate_callback(url)
            print(f"✅ Validated: {result}")
        except ValueError as e:
            print(f"❌ Invalid URL '{url}': {e}")