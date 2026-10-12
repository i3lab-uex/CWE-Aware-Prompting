#!/usr/bin/env python3
"""
Utility for validating external API URLs to mitigate SSRF (CWE‑918).

The module exposes a single function:
    verify_api_address(url_to_check: str) -> str

It ensures that the supplied URL:
* uses a safe scheme (http or https)
* resolves to an IP address that is not private, loopback, link‑local,
  multicast or unspecified
* belongs to a pre‑defined list of trusted domains

If any check fails, a ValueError is raised with an explanatory message.
"""

from __future__ import annotations

import socket
import ipaddress
import urllib.parse
from typing import List, Set


# ---------------------------- Configuration ---------------------------------

# Trusted domains that are allowed to be accessed.  The list can be extended
# as needed; domain names should not contain protocol prefixes or paths.
TRUSTED_DOMAINS: Set[str] = {
    "api.trusted.com",
    "services.example.org",
    # Add more trusted domains here
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_private_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """
    Return True if the IP address is private, loopback, link-local,
    multicast or unspecified.
    """
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
    )


def _resolve_hostname(hostname: str) -> List[ipaddress._BaseAddress]:
    """
    Resolve a hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns tuples: (family, socktype, proto, canonname, sockaddr)
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    ips: List[ipaddress._BaseAddress] = []
    for family, _, _, _, sockaddr in infos:
        # IPv4: sockaddr[0] is the address string
        # IPv6: sockaddr[0] is the address string
        addr_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(addr_str)
            ips.append(ip_obj)
        except ValueError:
            # Skip invalid addresses (should not happen)
            continue

    if not ips:
        raise ValueError(f"No valid IP addresses found for hostname '{hostname}'")
    return ips


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check if the hostname is exactly one of the trusted domains or a
    subdomain thereof.
    """
    # Normalise: lower case, strip trailing dot
    hostname = hostname.lower().rstrip(".")
    for domain in TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, unchanged from the input.

    Raises
    ------
    ValueError
        If the URL scheme is not allowed, if the hostname resolves to a
        private/internal IP address, or if the domain is not in the trusted list.
    """
    # Parse URL
    parsed = urllib.parse.urlparse(url_to_check)
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(parsed.hostname)

    # Ensure none of the resolved IPs are private/internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{parsed.hostname}' resolves to a private or internal IP address: {ip}"
            )

    # Check domain trust
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(
            f"Hostname '{parsed.hostname}' is not in the list of trusted domains"
        )

    # All checks passed; return the original URL
    return url_to_check


# ---------------------------- Example usage ---------------------------------
if __name__ == "__main__":
    # Example URLs (replace with real ones as needed)
    test_urls = [
        "https://api.trusted.com/v1/resource",
        "http://services.example.org/api/data",
        # The following should raise errors
        # "http://localhost/api",
        # "https://10.0.0.5/endpoint",
    ]

    for url in test_urls:
        try:
            validated = verify_api_address(url)
            print(f"✅ Validated: {validated}")
        except ValueError as e:
            print(f"❌ Validation failed for '{url}': {e}")