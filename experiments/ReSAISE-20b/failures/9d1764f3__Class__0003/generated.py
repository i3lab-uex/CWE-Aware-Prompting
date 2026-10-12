#!/usr/bin/env python3
"""
Utility to validate an external webhook URL before using it for internal API calls.
"""

import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: whitelist of allowed public API domains.
# --------------------------------------------------------------------------- #
WHITELISTED_DOMAINS = {
    "api.example.com",
    "hooks.service.org",
    # Add more approved domains here
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is in a private, loopback,
    link-local, or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_to_public_ip(hostname: str) -> bool:
    """
    Resolve a hostname to its IP addresses and ensure that at least one
    resolves to a public IP. Raise ValueError if all are private.
    """
    try:
        # getaddrinfo returns a list of tuples; the 4th element contains the IP
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for '{hostname}': {exc}") from None

    public_ip_found = False
    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if not _is_private_ip(ip):
            public_ip_found = True
            break

    if not public_ip_found:
        raise ValueError(f"All resolved IPs for '{hostname}' are private or reserved.")
    return True


def _normalize_url(parsed: urlparse) -> str:
    """
    Reconstruct the URL with a safe scheme (https) and strip fragments.
    Preserve user info if present but enforce https.
    """
    scheme = "https"
    netloc = parsed.netloc
    path = parsed.path or "/"
    params = parsed.params
    query = parsed.query
    fragment = ""  # discard fragments
    return urlunparse((scheme, netloc, path, params, query, fragment))


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a sanitized, secure URL
    suitable for internal API calls.

    Parameters:
        webhook_link (str): The raw external webhook URL.

    Returns:
        str: A validated and sanitized URL that is safe to use internally.

    Raises:
        ValueError: If the URL domain is not in the whitelist, or if it resolves
                    only to private/internal IP addresses.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    # Basic URL parsing
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {webhook_link}")

    # Enforce HTTPS scheme
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Extract hostname (strip port)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Could not determine hostname from URL: {webhook_link}")

    # Domain whitelist check (case-insensitive)
    if host.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist.")

    # Resolve hostname to IPs and ensure at least one public address
    _resolve_to_public_ip(host)

    # Reconstruct a sanitized URL (force https, drop fragments)
    safe_url = _normalize_url(parsed)

    return safe_url