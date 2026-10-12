#!/usr/bin/env python3
"""
Secure API URL inspection to mitigate SSRF and Confused‑Deputy attacks.
"""

from __future__ import annotations

import ipaddress
import socket
import ssl
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration – list of domains that are considered trusted.
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "api.trusted.com",
    "service.example.org",
    # Add more trusted domains as needed.
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or otherwise
    internal/sensitive."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    # Check for private, loopback, link-local, carrier-grade NAT,
    # multicast, and unspecified addresses.
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved  # includes carrier-grade NAT, etc.
        or addr.is_multicast
        or addr.is_unspecified
    )

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to its IPv4 and IPv6 addresses."""
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    return [info[4][0] for info in infos]

def _is_trusted_host(host: str) -> bool:
    """Check if the host is in the list of trusted domains."""
    # Exact match or subdomain check
    if host.lower() in TRUSTED_DOMAINS:
        return True

    # Allow subdomains of trusted domains
    for domain in TRUSTED_DOMAINS:
        if host.lower().endswith("." + domain):
            return True

    return False


# --------------------------------------------------------------------------- #
# Main inspection function
# --------------------------------------------------------------------------- #

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged).

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_inspect)

    # 1. Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP(S) are allowed.")

    # 2. Ensure netloc (host:port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # 3. Extract hostname (exclude port)
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to extract hostname from URL")

    # 4. Reject localhost or IP addresses that are internal
    if host.lower() in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Access to localhost is disallowed")

    # 5. Resolve hostname and check each IP
    for ip in _resolve_host(host):
        if _is_ip_private(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private/internal IP address ({ip})")

    # 6. Ensure host is in the trusted domain list
    if not _is_trusted_host(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains")

    # 7. (Optional) Verify that the SSL certificate matches the host if HTTPS
    if parsed.scheme == "https":
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, parsed.port or 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    # The SSL handshake succeeded; certificate is valid for the host
                    pass
        except Exception as exc:
            raise ValueError(f"SSL verification failed for host '{host}': {exc}") from exc

    # All checks passed; return the original URL
    return urlunparse(parsed)


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.trusted.com/v1/data",
        "http://service.example.org/api",
        "https://127.0.0.1/secret",          # should fail
        "http://untrusted.com/api",           # should fail
    ]

    for u in test_urls:
        try:
            validated = inspect_api_url(u)
            print(f"✅ Validated: {validated}")
        except ValueError as e:
            print(f"❌ Invalid URL '{u}': {e}")