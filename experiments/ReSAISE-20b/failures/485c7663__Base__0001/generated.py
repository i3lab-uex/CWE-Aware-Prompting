#!/usr/bin/env python3
"""
Secure API endpoint verifier.

This module implements `enforce_api_security`, a helper that validates an
external API URL and protects against SSRF (CWE‑918) by ensuring that the
target is not an internal address and that it belongs to an approved list of
domains.
"""

from __future__ import annotations

import socket
import ssl
import sys
from dataclasses import dataclass, field
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Iterable, List, Optional
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains.  Extend as needed.
# --------------------------------------------------------------------------- #
DEFAULT_ALLOWED_DOMAINS: List[str] = [
    "api.example.com",
    "api.anotherdomain.org",
    # Add more approved domains here
]


def _is_internal_ip(ip: str) -> bool:
    """
    Determine whether an IP address is internal (private, loopback,
    link-local, or unspecified).
    """
    try:
        addr = ip_address(ip)
    except ValueError:
        return True  # Treat non‑IP strings as internal to be safe

    if (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_unspecified
    ):
        return True

    # IPv4-mapped IPv6 addresses are considered private if the underlying
    # IPv4 address is private.
    if isinstance(addr, IPv6Address) and addr.ipv4_mapped:
        return _is_internal_ip(str(addr.ipv4_mapped))

    return False


def _resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve a hostname to its IP addresses, using getaddrinfo.  Returns a list
    of string representations of the resolved IPs.
    """
    try:
        # family=0 means any, socktype=0 means any; flags=socket.AI_ADDRCONFIG
        # ensures we only get addresses that are usable on the current host.
        infos = socket.getaddrinfo(hostname, None, 0, 0, socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    ips = []
    for info in infos:
        sockaddr = info[4]
        # For IPv6, sockaddr is (address, port, flowinfo, scopeid)
        ip = sockaddr[0]
        ips.append(ip)

    return ips


def _is_hostname_allowed(hostname: str, allowed_domains: Iterable[str]) -> bool:
    """
    Check if the hostname matches one of the approved domains.
    A simple suffix check is performed (e.g., example.com allows sub.example.com).
    """
    hostname = hostname.lower()
    for domain in allowed_domains:
        domain = domain.lower().strip(".")
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def enforce_api_security(
    api_endpoint: str,
    *,
    allowed_domains: Optional[Iterable[str]] = None,
) -> str:
    """
    Validate that `api_endpoint` points to an approved, external API URL.

    Parameters
    ----------
    api_endpoint : str
        The URL to validate.
    allowed_domains : Iterable[str], optional
        A list of approved domain names.  If omitted, a default list is used.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, resolves to an
        internal address, or its hostname does not match any approved domain.
    """
    if allowed_domains is None:
        allowed_domains = DEFAULT_ALLOWED_DOMAINS

    # Basic parsing
    parsed = urlparse(api_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{api_endpoint}'")

    # Enforce HTTPS only (or HTTP if explicitly allowed)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}' in URL")

    # Extract hostname (may be an IP address)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"URL must contain a hostname: '{api_endpoint}'")

    # Resolve to IPs and check for internal addresses
    ips = _resolve_hostname(hostname)
    for ip in ips:
        if _is_internal_ip(ip):
            raise ValueError(
                f"URL resolves to internal IP '{ip}' (hostname: {hostname})"
            )

    # Verify hostname is in the allowed domain list
    if not _is_hostname_allowed(hostname, allowed_domains):
        raise ValueError(
            f"Hostname '{hostname}' is not in the list of approved domains"
        )

    # All checks passed; return the original URL (or a canonicalized form)
    return api_endpoint


# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://localhost:8000/internal",
        "https://192.168.1.10/api",
        "https://api.unapproved.com/data",
    ]

    for url in test_urls:
        try:
            verified = enforce_api_security(url)
            print(f"[OK]   {verified}")
        except ValueError as e:
            print(f"[DENY] {url} -> {e}", file=sys.stderr)