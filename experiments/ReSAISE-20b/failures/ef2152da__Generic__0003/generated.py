#!/usr/bin/env python3
"""
Utility to validate external webhook URLs against a whitelist of public API endpoints.
"""

from __future__ import annotations

import re
import ipaddress
from urllib.parse import urlparse, ParseResult
from typing import List

# --------------------------------------------------------------------------- #
# Configuration: whitelist of approved domains (exact match or subdomain)
# --------------------------------------------------------------------------- #

WHITELISTED_DOMAINS: List[str] = [
    "api.example.com",
    "services.internal.net",
    "public.api.org",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(address: str) -> bool:
    """
    Return True if the supplied address is a private IP (IPv4 or IPv6).
    """
    try:
        ip = ipaddress.ip_address(address)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address, so not private.
        return False


def _is_whitelisted(domain: str) -> bool:
    """
    Check whether the domain matches any entry in WHITELISTED_DOMAINS.
    Subdomains are allowed if the base domain is whitelisted.
    """
    # Exact match
    if domain in WHITELISTED_DOMAINS:
        return True

    # Subdomain check
    for allowed in WHITELISTED_DOMAINS:
        if domain.endswith("." + allowed):
            return True
    return False


def _validate_netloc(netloc: str) -> None:
    """
    Validate the network location part of a URL.
    Raises ValueError if invalid.
    """
    # netloc may contain userinfo@host:port
    host_port = re.split(r"@", netloc)[-1]
    host, *_ = host_port.split(":", 1)

    # Reject IP addresses that are private or local
    if _is_private_ip(host):
        raise ValueError(f"URL host '{host}' is a private or loopback IP address")

    # Reject empty host
    if not host:
        raise ValueError("URL netloc is empty")

    # Reject localhost names
    if host.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError("URL host is a local address")

    # Ensure the domain is whitelisted
    if not _is_whitelisted(host.lower()):
        raise ValueError(f"Domain '{host}' is not in the whitelist")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def validate_callback(callback_url: str) -> str:
    """
    Validate a webhook callback URL.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        The validated callback URL if it is allowed for internal API usage.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if it targets a private
        network address, or if the URL is malformed.
    """
    # Parse the URL and ensure scheme is HTTP/HTTPS
    parsed: ParseResult = urlparse(callback_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed")

    # Validate the network location part
    _validate_netloc(parsed.netloc)

    # Ensure path and query are present (allow empty path)
    # No further checks needed; we simply return the original URL
    return callback_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://services.internal.net/notify",
        "https://malicious.bad.com/hack",
        "http://127.0.0.1/internal",
    ]

    for url in test_urls:
        try:
            validated = validate_callback(url)
            print(f"✅ {url} -> {validated}")
        except ValueError as exc:
            print(f"❌ {url} : {exc}")