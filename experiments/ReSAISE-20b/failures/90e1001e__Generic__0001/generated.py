#!/usr/bin/env python3
"""
Utility for validating URLs that point to approved external APIs.

The function ``validate_service_url`` performs several checks:
* The URL must use the HTTP or HTTPS scheme.
* The hostname must resolve to a public IP address that is not in
  private/reserved ranges.
* The hostname must be present in a whitelist of approved domains
  (supports exact match or wildcard subdomains).

If any check fails, a ``ValueError`` is raised.  On success the function
returns the normalized URL (scheme, host, path, query, fragment).
"""

from __future__ import annotations

import re
import socket
import sys
import urllib.parse
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Iterable, Set

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Whitelist of approved domains.
# Each entry can be:
#   * a literal domain name, e.g. "api.example.com"
#   * a wildcard prefix ending with "*", e.g. "*.trusted.org" matches
#     subdomains like "foo.trusted.org"
APPROVED_DOMAINS: Set[str] = {
    "api.example.com",
    "*.trusted.org",
    "service.safe.net",
}

# Regular expression to detect private/reserved IP ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 link-local and unique local
        (?:fe80::/10|fc00::/7)
    )$
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address string is private or reserved.
    Supports both IPv4 and IPv6.
    """
    try:
        addr = ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    if isinstance(addr, (IPv4Address, IPv6Address)):
        # ip_address has built‑in is_private and is_reserved
        return addr.is_private or addr.is_reserved

    return False


def _resolve_hostname(hostname: str) -> Iterable[str]:
    """
    Resolve a hostname to all IPv4 and IPv6 addresses.
    Returns an iterable of IP strings.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from None

    ips = set()
    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        ips.add(ip)
    return ips


def _is_domain_approved(hostname: str) -> bool:
    """
    Check if the hostname matches any entry in APPROVED_DOMAINS.
    Supports exact match and wildcard prefixes ending with '*'.
    """
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith("*."):
            # wildcard subdomain
            suffix = pattern[1:]  # remove leading '*'
            if hostname.endswith(suffix):
                return True
        else:
            if hostname == pattern:
                return True
    return False


# --------------------------------------------------------------------------- #
# Main validation function
# --------------------------------------------------------------------------- #

def validate_service_url(service_url: str) -> str:
    """
    Validate that *service_url* points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL does not use HTTP(S), resolves to a private IP,
        or its hostname is not in the approved domain list.
    """
    # Parse and validate scheme
    parsed = urllib.parse.urlparse(service_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"URL scheme must be http or https, got '{parsed.scheme}'")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Resolve host to IPs and ensure none are private
    resolved_ips = _resolve_hostname(hostname)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # Ensure hostname is approved
    if not _is_domain_approved(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the approved domain list")

    # Reconstruct URL to normalise it
    normalized = urllib.parse.urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return normalized


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://sub.trusted.org/api",
        "https://192.168.1.10/endpoint",  # should fail
    ]

    for url in test_urls:
        try:
            validated = validate_service_url(url)
            print(f"✅ {url} -> {validated}")
        except ValueError as e:
            print(f"❌ {url} : {e}", file=sys.stderr)