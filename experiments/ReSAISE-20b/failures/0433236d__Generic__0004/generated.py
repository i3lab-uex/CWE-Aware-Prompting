#!/usr/bin/env python3
"""
handle_webhook_request.py

Provides a single function that validates an external URL and returns it
only if it points to one of the approved public API domains.  The function
checks that the URL uses a safe scheme (http/https), that the hostname is in
the whitelist, and that it does not resolve to a private or loopback address.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, ParseResult


# --------------------------------------------------------------------------- #
# Configuration: whitelist of allowed public API domains
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS = {
    "api.example.com",
    "auth.service.org",
    "data.provider.net",
}

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def _is_private_ip(host: str) -> bool:
    """
    Resolve *host* to an IP address and determine if it is a private or
    loopback address.
    """
    try:
        # Resolve hostname to IP(s); use getaddrinfo for IPv4/IPv6
        addresses = socket.getaddrinfo(host, None)
    except socket.gaierror:
        # If we cannot resolve the host, treat it as unsafe
        return True

    for family, _, _, _, sockaddr in addresses:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
        except ValueError:
            # Skip invalid IPs (shouldn't happen)
            continue

    return False


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the hostname matches one of the allowed domains.
    Subdomains are considered invalid unless explicitly listed.
    """
    # Normalize host: strip trailing dot, lowercase
    host = host.rstrip(".").lower()
    return host in ALLOWED_DOMAINS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def handle_webhook_request(external_url: str) -> str:
    """
    Validate *external_url* and return it if it is safe for internal use.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        The validated URL that can be used for internal API requests.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, if the domain is not in the
        whitelist, or if it resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(external_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname).")

    # Separate hostname and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname.")

    # Check domain whitelist
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of allowed API endpoints.")

    # Check for private or loopback IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL resolves to a private or internal IP address: {host}")

    # Reconstruct the URL (in case the input had an unnormalized form)
    safe_url = parsed.geturl()

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://auth.service.org/login",
        "https://malicious.example.com/steal",
        "http://127.0.0.1:8000/internal",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = handle_webhook_request(url)
            print(f"  -> Allowed: {result}\n")
        except ValueError as e:
            print(f"  -> Rejected: {e}\n")