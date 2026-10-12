#!/usr/bin/env python3
"""
Utility to validate that a given API URL points to an external, trusted host.
The function protects against SSRF attacks by ensuring the hostname resolves
to a public IP and is in an approved list of domains.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.parse
from typing import Iterable, List


# --------------------------------------------------------------------------- #
# Configuration – list of domains that are considered trusted
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS: List[str] = [
    "api.example.com",
    "services.trusted.org",
    "data.api.gov",
]  # <-- extend this list as needed


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is public (not private, loopback,
    link-local, or reserved).
    """
    try:
        addr = ipaddress.ip_address(ip)
        return not (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
        )
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_public_ip(hostname: str) -> List[str]:
    """
    Resolve the hostname to a list of IP addresses and return only those that
    are public. Raises ValueError if none are public.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc

    public_ips = []
    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if _is_public_ip(ip):
            public_ips.append(ip)

    if not public_ips:
        raise ValueError(f"All resolved IPs for '{hostname}' are non‑public.")
    return public_ips


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check if the hostname ends with one of the trusted domains.
    Subdomains are allowed (e.g., api.sub.example.com is accepted if
    example.com is trusted).
    """
    hostname = hostname.lower()
    return any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def verify_api_address(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an untrusted domain,
        or resolves to a non‑public IP address.
    """
    # Basic parsing
    parsed = urllib.parse.urlparse(url_to_check)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"URL must use http or https scheme: '{url_to_check}'")

    if not parsed.netloc:
        raise ValueError(f"URL must contain a network location (host): '{url_to_check}'")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Could not extract hostname from URL: '{url_to_check}'")

    # Check against trusted domain list
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # Resolve hostname to IP(s) and ensure at least one public IP
    _resolve_public_ip(hostname)

    # All checks passed – return the original URL unchanged
    return url_to_check


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://services.trusted.org/api/data",
        "https://malicious.example.com/evil",
    ]

    for url in test_urls:
        try:
            valid = verify_api_address(url)
            print(f"[OK] {valid}")
        except ValueError as e:
            print(f"[FAIL] {url} -> {e}")