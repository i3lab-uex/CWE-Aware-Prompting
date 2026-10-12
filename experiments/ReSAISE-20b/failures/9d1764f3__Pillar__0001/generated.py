#!/usr/bin/env python3
"""
validate_webhook module

Provides a single function, validate_webhook(webhook_link: str) -> str,
which verifies that an incoming webhook URL points to a whitelisted
public API endpoint and does not target private or internal network
addresses.  If the URL passes validation, it is returned unchanged;
otherwise a ValueError is raised.

The implementation protects against CWE‑664 by ensuring that
the resource (the webhook URL) is fully validated before being used,
and no lingering references to the original untrusted input are kept.
"""

import ipaddress
import re
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Whitelisted public API domains (example list). Adjust to your real endpoints.
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.service.net",
    "hooks.myapp.org",
}

# Regular expression to match private IP ranges (RFC1918 + loopback & link-local)
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                                  # Loopback
    (^10\.)|                                   # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\. )|            # Class B private
    (^192\.168\.)|                             # Class C private
    (^169\.254\.)                              # Link-local
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is a private or non‑public IP address."""
    try:
        return not ipaddress.ip_address(ip_str).is_global
    except ValueError:
        # Not a valid IP address
        return True


def _is_private_hostname(hostname: str) -> bool:
    """Return True if hostname resolves to a private IP address."""
    # Resolve all possible IPs for the hostname
    try:
        import socket

        addrinfo = socket.getaddrinfo(hostname, None)
        for _, _, _, _, sockaddr in addrinfo:
            ip = sockaddr[0]
            if _is_private_ip(ip):
                return True
    except Exception:
        # If we cannot resolve, treat it as potentially unsafe
        return True
    return False


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL.

    Parameters
    ----------
    webhook_link : str
        The raw webhook URL supplied by an external source.

    Returns
    -------
    str
        The validated webhook URL, identical to the input if it passes checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑whitelisted domain, or resolves to
        a private/internal IP address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Ensure scheme is HTTPS (or HTTP if you allow it, but HTTPS is preferred)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname (netloc may contain port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Domain whitelist check (case-insensitive)
    if host.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Ensure the hostname does not resolve to a private IP
    if _is_private_hostname(host):
        raise ValueError(f"Hostname '{host}' resolves to a private IP address")

    # Optional: reject URLs containing obvious private IPs in the host part
    if PRIVATE_IP_RE.search(host):
        raise ValueError(f"Hostname '{host}' appears to be a private IP address")

    # All checks passed; return the original URL
    return webhook_link

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple self‑test
    test_urls = [
        "https://api.example.com/webhook",
        "http://webhooks.service.net/receive",
        "https://127.0.0.1/internal",  # should fail
        "https://unknown.com/hook",    # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            validated = validate_webhook(url)
            print("  -> Validated URL:", validated)
        except ValueError as exc:
            print(f"  -> Validation error: {exc}")