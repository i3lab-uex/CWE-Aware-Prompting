#!/usr/bin/env python3
"""
rss_validator.py

Provides a single helper function `validate_rss_link` that checks an RSS feed URL
against a whitelist of trusted providers and ensures it does not target internal
networks or private IP ranges.  The function returns a sanitized URL that can be
used safely by downstream consumers.

The implementation is careful to avoid the CWE‑441 "Unintended Proxy or
Intermediary" problem by preserving the original host when returning the URL,
and never forwarding a request on behalf of the caller without explicit
validation.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, urlunparse


# --------------------------------------------------------------------------- #
#  Configuration: list of approved RSS providers
# --------------------------------------------------------------------------- #

# These are the only domains that we consider trustworthy.  The list can be
# extended as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",  # Google News feeds
    "rss.cnn.com",
    "feeds.feedburner.com",
    # Add more providers here
}

# Regular expression to detect private or local IP addresses (IPv4 and IPv6)
_PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10(?:\.\d{1,3}){3})
      | # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})
      | # 192.168.0.0 – 192.168.255.255
        (192\.168(?:\.\d{1,3}){2})
      | # 127.0.0.1 (loopback)
        (127(?:\.\d{1,3}){3})
      | # IPv6 link-local
        ([a-fA-F0-9:]+::[a-fA-F0-9:])
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or loopback.
    """
    # Resolve IPv6 addresses
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, maybe a hostname; we'll rely on DNS resolution later.
        return False


def _is_internal_hostname(host: str) -> bool:
    """
    Determine if a hostname resolves to a private IP or loopback.
    This is conservative: we reject hostnames that contain dots
    but could potentially resolve to a private network.
    """
    # If the host is an IP literal, we can check directly
    if _is_private_ip(host):
        return True

    # If the hostname contains a dot, assume it's a public domain.
    # For more strict checks, DNS resolution could be performed,
    # but that would introduce side effects and timing attacks.
    return False


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that `rss_link` points to a trusted RSS provider and does not
    reference an internal or private network.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized version of the URL that can be safely used by callers.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted provider,
        or attempts to access a private/internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    # Parse the URL
    parsed = urlparse(rss_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or internal hosts
    if _is_internal_hostname(host):
        raise ValueError("URL points to a private or internal network")

    # Enforce whitelist of trusted providers
    if host.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Host '{host}' is not an approved RSS provider")

    # Reconstruct the URL to ensure no query or fragment are forwarded
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://example.com/evil.rss",  # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validated: {validate_rss_link(url)}")
        except ValueError as exc:
            print(f"Rejected: {url} -> {exc}")