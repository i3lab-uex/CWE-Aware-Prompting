#!/usr/bin/env python3
"""
Utility to validate external webhook URLs before they are used in internal API calls.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Whitelist configuration – only these hostnames are allowed for internal
# communication. Adjust as required.
WHITELISTED_HOSTNAMES = {
    "api.example.com",
    "service.internal.net",
    "public.api.org",
}

# --------------------------------------------------------------------------- #
# Regular expression for detecting private or reserved IP addresses.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                               # Start of non-capturing group for all private ranges
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |   # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0 – 172.31.255.255
        192\.168\.\d{1,3}\.\d{1,3} |   # 192.168.0.0 – 192.168.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |   # localhost
        169\.254\.\d{1,3}\.\d{1,3} |   # link-local
        0\.\d{1,3}\.\d{1,3}\.\d{1,3} |   # unspecified
        255\.255\.255\.255              # broadcast
    )
    $
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_private_ip(host: str) -> bool:
    """
    Determine if a hostname resolves to a private IP address.

    Args:
        host: Hostname or IP string.

    Returns:
        True if the address is private, False otherwise.
    """
    # Attempt to interpret as an IP first
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP literal; try regex for known private patterns
        return bool(PRIVATE_IP_REGEX.match(host))


def _is_whitelisted_hostname(host: str) -> bool:
    """
    Check if the hostname is in the approved whitelist.

    Args:
        host: Hostname string (case-insensitive).

    Returns:
        True if allowed, False otherwise.
    """
    return host.lower() in WHITELISTED_HOSTNAMES


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it can be used for internal API calls.

    The function checks that the scheme is HTTPS, the hostname is on a whitelist,
    and that it does not resolve to any private or internal network addresses.
    It returns the original URL if all checks pass.

    Args:
        webhook_endpoint: External webhook URL string.

    Returns:
        The validated and safe URL.

    Raises:
        ValueError: If the URL is malformed, not HTTPS,
                    has a non-whitelisted domain, or targets private network.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    # Basic URL sanity
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Enforce HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against whitelist
    if not _is_whitelisted_hostname(host):
        raise ValueError(f"Hostname '{host}' is not in the approved whitelist")

    # Reject private or internal IPs
    if _is_private_ip(host):
        raise ValueError(f"Hostname '{host}' resolves to a private IP address")

    # Rebuild URL to ensure normalisation (e.g., strip default ports)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,  # netloc already includes host:port
            parsed.path or "",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple self‑test
    test_urls = [
        "https://api.example.com/webhook",
        "http://api.example.com/webhook",           # Should fail (HTTP)
        "https://malicious.com/attack",
        "https://127.0.0.1/internal",
    ]

    for url in test_urls:
        try:
            print(f"✅ {verify_webhook(url)}")
        except ValueError as e:
            print(f"❌ {url} -> {e}")