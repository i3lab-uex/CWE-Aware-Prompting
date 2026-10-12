#!/usr/bin/env python3
"""
Secure API URL inspector.

This module provides a single helper function `inspect_api_url` that verifies
that an API URL points to a trusted external domain and does not resolve to any
private or loopback IP address.  The function raises a ValueError if the URL
fails validation, otherwise it returns the original URL unchanged.

The implementation performs a number of safety checks:

1. Scheme must be `http` or `https`.
2. The hostname is resolved to an IP address.
3. The resolved IP must not be a private, loopback or reserved address
   (RFC 1918, RFC 5735, etc.).
4. The hostname must match a list of explicitly trusted domains.
"""

import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration – add trusted domains here
# --------------------------------------------------------------------------- #

TRUSTED_DOMAINS = {
    "api.example.com",
    "api.trustedservice.io",
    "data.safe-api.net",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_ip_private(ip: str) -> bool:
    """
    Determine if an IP address string is private, loopback or otherwise
    non‑public. Uses the socket.inet_aton and struct unpack to check the
    standard private ranges.
    """
    import ipaddress

    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address – treat as unsafe.
        return True


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, the hostname does not resolve,
        resolves to a private or reserved IP, or is not in TRUSTED_DOMAINS.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_inspect)

    # 1. Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    # 2. Hostname extraction
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # 3. Resolve the hostname
    try:
        ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # 4. Check each resolved IP
    for ip in ips:
        if _is_ip_private(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP '{ip}', which is disallowed.")

    # 5. Trusted domain check (case-insensitive)
    if hostname.lower() not in {d.lower() for d in TRUSTED_DOMAINS}:
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains.")

    # 6. Normalise URL (remove default ports)
    netloc = hostname
    if parsed.port:
        # Include port only if it's non‑standard for the scheme
        default_port = 443 if parsed.scheme.lower() == "https" else 80
        if parsed.port != default_port:
            netloc = f"{hostname}:{parsed.port}"
    normalized = urlunparse((
        parsed.scheme.lower(),
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return normalized


# --------------------------------------------------------------------------- #
# Example usage (for debugging / testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://api.trustedservice.io:8080/data",
        "https://malicious.local/endpoint",          # should fail
        "ftp://api.example.com/resource",            # should fail
    ]

    for url in test_urls:
        try:
            print(f"✅ {inspect_api_url(url)}")
        except ValueError as exc:
            print(f"❌ {url} -> {exc}")