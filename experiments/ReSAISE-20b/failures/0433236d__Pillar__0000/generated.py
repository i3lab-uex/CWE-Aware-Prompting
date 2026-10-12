#!/usr/bin/env python3
"""
A secure webhook URL handler that validates external URLs against an allowed domain list
and ensures they do not target private or internal networks.
"""

from __future__ import annotations

import re
import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
from urllib.parse import urlparse, ParseResult

# --------------------------------------------------------------------------- #
# Configuration: allowed public API domains (regex or exact matches)
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS = {
    "api.example.com",
    "public.api.service.org",
    r"^https?://(?:[a-zA-Z0-9-]+\.)*trusted-domain\.net$",
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host matches any entry in ALLOWED_DOMAINS.
    Entries can be exact strings or compiled regular expressions.
    """
    for pattern in ALLOWED_DOMAINS:
        if isinstance(pattern, str):
            # Treat as exact match
            if host.lower() == pattern.lower():
                return True
        else:
            # Treat as regex
            if re.match(pattern, host.lower()):
                return True
    return False


def _is_public_ip(host: str) -> bool:
    """
    Resolve host to IP addresses and ensure none are private, loopback,
    or link-local. Raises ValueError if resolution fails.
    """
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ip_address(ip_str)
        except ValueError as exc:  # pragma: no cover
            raise ValueError(f"Invalid IP address '{ip_str}' resolved for host '{host}': {exc}") from exc

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            raise ValueError(f"IP address '{ip_str}' for host '{host}' is not publicly routable")

    return True


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return it for internal use.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated, sanitized URL safe for internal API consumption.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        references a disallowed domain, or resolves to a private IP.
    """
    if not isinstance(external_url, str):
        raise ValueError("URL must be a string")

    # Parse URL
    parsed: ParseResult = urlparse(external_url.strip())
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Domain validation
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the allowed list")

    # IP resolution check
    _is_public_ip(parsed.hostname)

    # Reconstruct URL to ensure canonical form
    safe_url = parsed.geturl()
    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (for local testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://public.api.service.org/notify",
        "https://malicious.com/hack",
    ]

    for url in test_urls:
        try:
            print(f"Validated URL: {handle_webhook_request(url)}")
        except ValueError as e:
            print(f"Validation failed for '{url}': {e}")