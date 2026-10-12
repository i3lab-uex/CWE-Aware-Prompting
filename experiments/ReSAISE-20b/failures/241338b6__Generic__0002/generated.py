#!/usr/bin/env python3
"""
Utility to verify that a given URL points to an approved external API.

The function performs several checks:

1. Validates that the scheme is http or https.
2. Confirms that the hostname resolves to a public IP address
   (not within private, loopback or reserved ranges).
3. Ensures that the hostname belongs to an approved domain list.

If any of these checks fail, a ValueError is raised.  On success,
the original URL is returned unchanged.
"""

import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains.  Add or remove entries as needed.
APPROVED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "data.api.trusted.net",
}

# Private / non‑public IP ranges (RFC 1918, loopback, link local, etc.)
PRIVATE_IP_RANGES = [
    ("10.0.0.0",   "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0","192.168.255.255"),
    ("127.0.0.0",  "127.255.255.255"),
    ("169.254.0.0","169.254.255.255"),
]

def _ip_in_private_range(ip: str) -> bool:
    """Return True if the IP address falls within a known private range."""
    import ipaddress
    ip_obj = ipaddress.ip_address(ip)
    for start, end in PRIVATE_IP_RANGES:
        if ip_obj >= ipaddress.ip_address(start) and ip_obj <= ipaddress.ip_address(end):
            return True
    return False

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an approved external API.

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
        If the URL does not use http/https, resolves to a private address,
        or its hostname is not in the approved domain list.
    """
    # 1. Parse URL and validate scheme
    parsed = urlparse(url_to_check)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # 2. Resolve the hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from None

    # 3. Ensure at least one public IP address
    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if not _ip_in_private_range(ip):
            break
    else:
        raise ValueError(f"Hostname {parsed.hostname} resolves only to private IPs")

    # 4. Verify hostname against approved domains
    if parsed.hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname {parsed.hostname} is not an approved domain")

    return url_to_check

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and quick test
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://localhost:8000/api",
        "https://10.0.0.5/secret",
    ]

    for u in test_urls:
        try:
            result = verify_api_link(u)
            print(f"✅ {u} -> {result}")
        except ValueError as e:
            print(f"❌ {u} : {e}")