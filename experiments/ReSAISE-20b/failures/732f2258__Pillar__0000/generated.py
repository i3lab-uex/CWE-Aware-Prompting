#!/usr/bin/env python3
"""
Utility for validating webhook URLs supplied by external services.

The function ``analyze_webhook`` ensures that the supplied URL:
* uses an approved public API domain.
* does not point to a private or internal network address (IPv4/IPv6).
* is safe for use in internal API requests.

If any of these checks fail a ``ValueError`` is raised.
"""

from __future__ import annotations

import re
import socket
import urllib.parse
import ipaddress
from typing import List, Set

# --------------------------------------------------------------------------- #
# Configuration: list of approved public API domains.
# --------------------------------------------------------------------------- #

ALLOWED_DOMAINS: Set[str] = {
    "api.example.com",
    "webhook.provider.net",
    "hooks.service.org",
}

# Regular expression to validate an HTTP/HTTPS URL
_URL_RE = re.compile(
    r"""
    ^(?P<scheme>https?)://               # http or https scheme
    (?P<host>[^:/?#]+)                   # host (hostname or IP)
    (:(?P<port>\d+))?                    # optional port
    (?P<path>/[^?#]*)?                   # optional path
    (\?(?P<query>[^#]*))?                # optional query
    (#(?P<fragment>.*))?$                # optional fragment
    """,
    re.IGNORECASE | re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(host: str) -> bool:
    """
    Determine whether a host string is a private IP address.
    Handles both IPv4 and IPv6 literals.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP literal; return False to allow DNS resolution check later
        return False


def _resolve_hostname(host: str) -> List[str]:
    """
    Resolve a hostname to its IPv4/IPv6 addresses.
    Raises socket.gaierror if resolution fails.
    """
    return list(set(socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)))


def _is_hostname_allowed(host: str) -> bool:
    """
    Check if the hostname (or its registered domain) is in the allowed list.
    For simplicity, we consider only the host itself; subdomains are accepted
    if they match exactly one of the allowed domains.
    """
    return host.lower() in ALLOWED_DOMAINS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return the sanitized, absolute URL.

    Parameters
    ----------
    webhook_address : str
        The raw URL string supplied by an external service.

    Returns
    -------
    str
        A validated, absolute URL suitable for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved domain,
        or points to a private/internal network address.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("Webhook address must be a string")

    match = _URL_RE.match(webhook_address.strip())
    if not match:
        raise ValueError("Malformed URL")

    scheme = match.group("scheme").lower()
    host = match.group("host")
    port = match.group("port")
    path = match.group("path") or ""
    query = f"?{match.group('query')}" if match.group("query") else ""

    # Reject private IP addresses directly
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Resolve hostname to ensure it does not resolve to a private IP
    try:
        addr_info = _resolve_hostname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from None

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback:
            raise ValueError("Hostname resolves to a private IP address")

    # Verify domain is allowed
    if not _is_hostname_allowed(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct the URL to ensure canonical form
    netloc = f"{host}:{port}" if port else host
    sanitized_url = urllib.parse.urlunparse((scheme, netloc, path, "", query[1:] if query else "", ""))

    return sanitized_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://localhost:8080/notify",
        "https://192.168.1.10/hook",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print("Result:", analyze_webhook(url))
        except ValueError as e:
            print(f"Rejected: {e}")
        print("-" * 40)