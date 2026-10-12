#!/usr/bin/env python3
"""
Utility to validate external API URLs and guard against SSRF (CWE‑918).

The `inspect_api_url` function checks that the supplied URL:
* uses an allowed scheme (`http`, `https`);
* does not point to a private, loopback or link‑local IP address;
* resolves to an IP that is not internal or reserved; and
* belongs to a list of trusted domains (or their sub‑domains).

If any check fails, a ValueError is raised.  Otherwise the original URL
is returned unchanged.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, ParseResult


# --------------------------------------------------------------------------- #
# Configuration – modify as appropriate for your environment
# --------------------------------------------------------------------------- #

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# Trusted domain patterns.  Sub‑domains are automatically allowed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.internal.company.com",
    # Add more domains as needed
}

# List of IP networks that are considered internal / non‑public.
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),          # loopback
    ipaddress.ip_network("169.254.0.0/16"),       # link‑local
    ipaddress.ip_network("::1/128"),             # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),            # Unique local address (ULA)
]


def _is_private_ip(ip: ipaddress._BaseAddress) -> bool:
    """
    Return True if the IP address is within a private or reserved network.
    """
    for net in PRIVATE_NETWORKS:
        if ip in net:
            return True
    return False


def _resolve_host(host: str) -> list[ipaddress._BaseAddress]:
    """
    Resolve a hostname to all its IP addresses (IPv4 and IPv6).
    Raises socket.gaierror if resolution fails.
    """
    # getaddrinfo returns tuples: (family, type, proto, canonname, sockaddr)
    addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    ips = []
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ips.append(ipaddress.ip_address(ip_str))
        except ValueError:
            # Skip invalid IPs (should not happen)
            continue
    return ips


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that `url_to_inspect` points to a trusted external API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not valid, uses a disallowed scheme,
        resolves to a private IP, or is outside the trusted domains.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(url_to_inspect)

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed scheme '{parsed.scheme}'. Only {ALLOWED_SCHEMES} are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host).")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL.")

    # Resolve the hostname
    try:
        resolved_ips = _resolve_host(host)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{host}': {exc}") from exc

    if not resolved_ips:
        raise ValueError(f"No IP addresses found for host '{host}'.")

    # Check each resolved IP
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or reserved, which is disallowed.")

    # Check domain trust
    host_lower = host.lower()
    if not any(host_lower == trusted or host_lower.endswith("." + trusted)
               for trusted in TRUSTED_DOMAINS):
        raise ValueError(f"Host '{host}' is not in the list of trusted domains.")

    # All checks passed – return the original URL
    return url_to_inspect


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://localhost/api",               # should fail
        "https://192.168.1.10/resource",       # should fail
        "https://service.internal.company.com/health",
    ]

    for url in test_urls:
        try:
            print(f"✔️  {inspect_api_url(url)}")
        except ValueError as e:
            print(f"❌  {url} → {e}")