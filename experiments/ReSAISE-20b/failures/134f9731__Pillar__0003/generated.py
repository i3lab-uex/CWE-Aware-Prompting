#!/usr/bin/env python3
"""
Utility for validating external webhook URLs before using them internally.
"""

import re
import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: list of approved public API endpoints (domain names only)
# --------------------------------------------------------------------------- #
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.partner.org",
    "services.trusted.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Determine whether the given IP address is in a private or reserved range.
    Supports both IPv4 and IPv6.

    Args:
        ip: IP address string

    Returns:
        True if the IP is private or reserved, False otherwise.
    """
    # IPv4 private ranges
    private_ipv4 = (
        re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
        re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
        re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    )
    if any(p.match(ip) for p in private_ipv4):
        return True

    # IPv6 unique local addresses (fc00::/7)
    if ip.lower().startswith("fc") or ip.lower().startswith("fd"):
        return True

    # Loopback addresses
    if ip == "127.0.0.1" or ip.lower() == "::1":
        return True

    # Link-local IPv6 (fe80::/10)
    if ip.lower().startswith("fe80"):
        return True

    # Reserved addresses (e.g., 0.0.0.0, 255.255.255.255)
    reserved = {"0.0.0.0", "255.255.255.255"}
    if ip in reserved:
        return True

    return False


def _resolve_host(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.

    Args:
        hostname: DNS name

    Returns:
        List of IP strings.
    """
    try:
        # getaddrinfo returns tuples; we extract the address part
        return [
            addr[4][0]
            for addr in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        ]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{hostname}': {exc}") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it is used internally.

    The function ensures that the URL:
      * Uses HTTPS or HTTP.
      * Has a hostname present in the WHITELISTED_DOMAINS set.
      * Does not resolve to a private or reserved IP address.

    Args:
        webhook_endpoint: The raw URL string supplied by an external source.

    Returns:
        A fully parsed, validated URL string ready for internal use.

    Raises:
        ValueError: If the URL is malformed, uses an unapproved domain,
                    or resolves to a private/internal IP.
    """
    # Basic parsing
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{webhook_endpoint}'")

    # Enforce HTTP or HTTPS only
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}' in '{webhook_endpoint}'")

    # Strip port for domain comparison
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError(f"URL missing hostname: '{webhook_endpoint}'")

    # Domain whitelist check
    if hostname not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

    # Resolve hostname and ensure no private IPs
    resolved_ips = _resolve_host(hostname)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to private IP address '{ip}', "
                "which is not allowed for external webhooks"
            )

    # Reconstruct the URL to normalize it
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{hostname}{':' + str(parsed.port) if parsed.port else ''}",
    ).geturl()

    return normalized


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         url = verify_webhook("https://api.example.com/webhooks/receive")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")