#!/usr/bin/env python3
"""
Utility for guarding against SSRF attacks by validating external API URLs.

The function `enforce_api_security` checks that a URL:
  * Uses http or https.
  * Resolves to an IP address outside of private, loopback, link‑local,
    or reserved ranges.
  * Belongs to a domain that is explicitly whitelisted.

If any of these checks fail, a ValueError is raised.
"""

import re
import socket
from urllib.parse import urlparse
import ipaddress
from typing import Set

# --------------------------------------------------------------------------- #
# Whitelist of approved domains.  Add or remove entries as your policy
# requires.
#
# Example:
#   APPROVED_DOMAINS = {"api.example.com", "services.mycorp.io"}
#
# The whitelist can be extended at runtime via `add_to_whitelist`.
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS: Set[str] = set()

def add_to_whitelist(domain: str) -> None:
    """
    Add a domain to the approved whitelist.

    Parameters
    ----------
    domain : str
        Domain name (e.g. "api.example.com"). Subdomains are treated as
        separate entries, so if you want to allow all sub‑domains you can
        use a pattern like "*.example.com" and the check will handle it.
    """
    domain = domain.lower().strip()
    if not domain:
        raise ValueError("Domain must be a non‑empty string")
    APPROVED_DOMAINS.add(domain)


def _is_domain_approved(hostname: str) -> bool:
    """
    Determine whether a hostname matches an entry in the whitelist.

    Supports exact matches and wildcard prefixes (e.g. "*.example.com").
    """
    hostname = hostname.lower()
    if hostname in APPROVED_DOMAINS:
        return True
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith("*."):
            # Wildcard match: check suffix after '*.'
            suffix = pattern[1:]  # includes the dot
            if hostname.endswith(suffix):
                return True
    return False


def _is_ip_allowed(ip: str) -> bool:
    """
    Validate that an IP address is not in a private, loopback,
    link‑local, or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False

    # Reject private, loopback, link-local, reserved, multicast, etc.
    if (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
    ):
        return False

    # IPv6 Unique Local Addresses (ULA) are also private.
    if addr.version == 6 and addr.is_private:
        return False

    return True


def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied API endpoint is safe to call.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs verification. It must use http or https.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a disallowed IP address, or its hostname
        is not in the approved whitelist.
    """
    if not isinstance(api_endpoint, str):
        raise ValueError("api_endpoint must be a string")

    parsed = urlparse(api_endpoint.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme; only http and https are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Resolve the hostname to all IP addresses (IPv4 & IPv6)
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {hostname!r}: {exc}") from exc

    # Ensure at least one resolved IP is allowed
    if not any(_is_ip_allowed(ai[4][0]) for ai in addrinfo):
        raise ValueError(f"Hostname {hostname!r} resolves to disallowed IP addresses")

    # Verify the hostname is in the approved whitelist
    if not _is_domain_approved(hostname):
        raise ValueError(f"Hostname {hostname!r} is not in the approved domain list")

    # All checks passed
    return api_endpoint


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Populate whitelist for demonstration
    add_to_whitelist("api.example.com")
    add_to_whitelist("*.trusted.io")

    test_urls = [
        "https://api.example.com/v1/resource",
        "http://malicious.internal.local/",
        "https://10.0.0.5/api",
        "ftp://api.example.com/resource",
    ]

    for url in test_urls:
        try:
            safe_url = enforce_api_security(url)
            print(f"[OK]   {safe_url}")
        except ValueError as e:
            print(f"[FAIL] {url} -> {e}")