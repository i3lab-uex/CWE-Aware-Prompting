#!/usr/bin/env python3
"""
verify_api_address.py

A utility to validate that a given URL points to an externally trusted API
endpoint, protecting against Server‑Side Request Forgery (SSRF) attacks.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: list of trusted domain names or subdomains.
#
# In a real application this should be externalised (e.g. config file, env
# variable, or a secrets manager).  For demonstration purposes we keep it in
# source code.  Domain matching is case‑insensitive.
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.partner.org",
    # Add more trusted domains here
}

# --------------------------------------------------------------------------- #
def _is_trusted_domain(host: str) -> bool:
    """
    Return True if the host ends with a domain in TRUSTED_DOMAINS.
    """
    host_lower = host.lower()
    return any(host_lower == d or host_lower.endswith("." + d) for d in TRUSTED_DOMAINS)


def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is not private, loopback or reserved.
    """
    addr = ipaddress.ip_address(ip)
    return not (addr.is_private or addr.is_loopback or addr.is_reserved)


def _resolve_host_to_public_ip(host: str) -> str:
    """
    Resolve the hostname to an IP address and ensure it is public.
    Raises ValueError if resolution fails or the IP is non‑public.
    """
    try:
        # Resolve to IPv4 and IPv6 addresses
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # Pick the first address that is public
    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if _is_public_ip(ip):
            return ip

    raise ValueError(f"All resolved IPs for host '{host}' are private or reserved.")


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that *url_to_check* points to an externally trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        A normalized, validated URL that is safe for outbound HTTP requests.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/loopback IP address.
    """
    if not url_to_check:
        raise ValueError("Empty URL provided")

    parsed = urlparse(url_to_check)

    # Basic scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Normalize the hostname (strip port for domain check)
    host = parsed.hostname
    if not host:
        raise ValueError("Could not parse hostname from URL")

    # 1. Check that the host is a trusted domain
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # 2. Resolve to IP and ensure it is public
    _resolve_host_to_public_ip(host)

    # 3. Reconstruct the URL to guarantee consistent formatting
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
    )
    return urlunparse(cleaned)


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demo usage
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://data.partner.org/api?x=1",
        "https://malicious.internal.local/endpoint",
    ]

    for url in test_urls:
        try:
            valid = verify_api_address(url)
            print(f"VALID:   {valid}")
        except ValueError as e:
            print(f"INVALID: {url} -> {e}")