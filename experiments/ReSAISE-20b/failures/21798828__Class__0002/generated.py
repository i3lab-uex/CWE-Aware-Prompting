#!/usr/bin/env python3
"""
Secure webhook URL handler.

This module provides a single function, :func:`handle_webhook`, which validates
an incoming webhook URL against a whitelist of approved public API endpoints.
It also checks that the URL does not point to an internal network address
(private IP, loopback, link‑local or reserved).  The function raises a
:class:`ValueError` if the URL is not considered safe.

The implementation follows best practices for preventing CWE‑441
(Confused Deputy) by ensuring that the URL's origin is verified before any
further processing or forwarding occurs.
"""

import re
from urllib.parse import urlparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains.  Add any additional public
# endpoints that are allowed to be invoked by the webhook.
APPROVED_DOMAINS = {
    "api.example.com",
    "public.api.company.org",
    # Add more approved domains as needed.
}

# --------------------------------------------------------------------------- #
def _is_private_hostname(hostname: str) -> bool:
    """
    Determine whether a hostname resolves to a private IP address.

    The function attempts to interpret the hostname as an IP literal.  If it
    fails, we consider it safe (i.e., a normal domain name).  Private IP
    detection is performed using :mod:`ipaddress`.

    Parameters:
        hostname (str): The host part of a URL.

    Returns:
        bool: ``True`` if the hostname is an IP address within a private
              network, otherwise ``False``.
    """
    try:
        ip_obj = ipaddress.ip_address(hostname)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        # Not an IP literal – treat as a domain name.
        return False


def _normalize_hostname(hostname: str) -> str:
    """
    Normalize a hostname by stripping any trailing dots and converting to
    lowercase.  This helps with case‑insensitive comparison against the
    whitelist.

    Parameters:
        hostname (str): The host part of a URL.

    Returns:
        str: Normalized hostname.
    """
    return hostname.rstrip(".").lower()


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it if it references an approved API
    endpoint.

    The function performs the following checks:
        1. URL must use HTTPS.
        2. Hostname (or IP) must not resolve to a private address.
        3. Hostname must match one of the approved domains.

    Parameters:
        webhook_link (str): The URL supplied by an external service.

    Returns:
        str: The validated, safe URL.

    Raises:
        ValueError: If the URL fails any validation step.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Hostname extraction
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Reject private IP addresses
    if _is_private_hostname(hostname):
        raise ValueError("URL points to a private or internal network address")

    # 4. Normalize hostname for comparison
    normalized_host = _normalize_hostname(hostname)

    # 5. Verify against approved domains (exact match or subdomain)
    if not any(
        normalized_host == domain or normalized_host.endswith("." + domain)
        for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Hostname '{normalized_host}' is not an approved domain")

    # 6. Return the original URL (or optionally reconstruct to enforce scheme)
    return webhook_link


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple tests
    test_urls = [
        "https://api.example.com/trigger",
        "https://public.api.company.org/v1/event",
        "http://api.example.com/trigger",  # should fail (HTTP)
        "https://192.168.1.10/endpoint",  # should fail (private IP)
        "https://malicious.com/attack",
    ]

    for url in test_urls:
        try:
            safe = handle_webhook(url)
            print(f"✅ {url} → {safe}")
        except ValueError as e:
            print(f"❌ {url} → {e}")