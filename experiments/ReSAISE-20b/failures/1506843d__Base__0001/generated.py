#!/usr/bin/env python3
"""
inspect_api_url.py

A helper function to validate that a supplied API URL points to an external,
trusted domain and does not resolve to private or internal network addresses.
This mitigates SSRF (CWE‑918) attacks.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.parse
from typing import Iterable, List


# --------------------------------------------------------------------------- #
# Trusted domain list – update this with your own domains
# --------------------------------------------------------------------------- #
_TRUSTED_DOMAINS: List[str] = [
    "api.example.com",
    "auth.myservice.org",
    "data.provider.net",
]

# --------------------------------------------------------------------------- #
# Private / non‑routable IP networks (RFC 1918, loopback, link‑local, etc.)
# --------------------------------------------------------------------------- #
_PRIVATE_NETWORKS: List[ipaddress.IPv4Network] = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # Loopback
    ipaddress.ip_network("169.254.0.0/16"),  # Link‑local
    ipaddress.ip_network("::1/128"),        # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),       # Unique local addresses (ULA)
]


def _is_ip_private(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Return True if the IP address is private or non‑routable."""
    for net in _PRIVATE_NETWORKS:
        if ip in net:
            return True
    return False


def _resolve_hostname(hostname: str) -> List[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    """
    Resolve a hostname to all its IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc

    ips: List[ipaddress.IPv4Address | ipaddress.IPv6Address] = []
    for entry in addr_info:
        family, _, _, _, sockaddr = entry
        ip_str = sockaddr[0]
        if family == socket.AF_INET:
            ips.append(ipaddress.IPv4Address(ip_str))
        elif family == socket.AF_INET6:
            ips.append(ipaddress.IPv6Address(ip_str))
    return ips


def _validate_scheme(scheme: str) -> None:
    """Ensure the URL uses http or https."""
    if scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{scheme}'. Only http/https allowed.")


def _validate_domain(domain: str) -> None:
    """Ensure the domain is in the trusted list."""
    if not any(domain.lower() == tld or domain.lower().endswith("." + tld) for tld in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not in the list of trusted domains.")


def _validate_ip_addresses(ips: Iterable[ipaddress.IPv4Address | ipaddress.IPv6Address]) -> None:
    """Ensure none of the resolved IPs are private or non‑routable."""
    for ip in ips:
        if _is_ip_private(ip):
            raise ValueError(f"Resolved IP address {ip} is private or non‑routable.")


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate. Must use http or https, point to a trusted domain,
        and resolve to at least one routable IP address.

    Returns
    -------
    str
        The original URL if it passes all validation checks.

    Raises
    ------
    ValueError
        If the URL fails any of the validation checks.
    """
    # Parse the URL and perform basic sanity checks
    parsed = urllib.parse.urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{url_to_inspect}'")

    # 1. Validate scheme
    _validate_scheme(parsed.scheme)

    # 2. Validate domain against trusted list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"URL does not contain a valid hostname: '{url_to_inspect}'")
    _validate_domain(hostname)

    # 3. Resolve hostname to IP addresses
    resolved_ips = _resolve_hostname(hostname)

    # 4. Ensure no private IPs are returned
    _validate_ip_addresses(resolved_ips)

    # If all checks pass, return the original URL
    return url_to_inspect


# --------------------------------------------------------------------------- #
# Example usage / test harness (uncomment to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://localhost:8000/health",
        "https://10.0.0.5/api",
    ]

    for u in test_urls:
        try:
            validated = inspect_api_url(u)
            print(f"✅ Validated: {validated}")
        except ValueError as e:
            print(f"❌ Validation failed for '{u}': {e}")