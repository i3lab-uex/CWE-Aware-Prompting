#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

The `secure_feed_link` function ensures that only URLs belonging to a
predefined list of trusted providers are accepted.  It also guards against
access to private or internal network addresses.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: trusted providers and restrictions
# --------------------------------------------------------------------------- #

# A set of allowed hostnames (case‑insensitive).
TRUSTED_HOSTNAMES = {
    "feeds.nytimes.com",
    "rss.cnn.com",
    "news.google.com/rss",
    "www.bbc.co.uk/news/10628494",
    "feeds.bbci.co.uk",  # example
}

# Regular expression to detect private IP ranges (RFC1918)
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:                             # start of string
        10\.                                # 10.0.0.0/8
      | 172\.(?:1[6-9]|2\d|3[0-1])\.         # 172.16.0.0/12
      | 192\.168\.                          # 192.168.0.0/16
    )
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(host: str) -> bool:
    """
    Determine if the host is a private IP address.
    Supports IPv4 and IPv6.
    """
    try:
        # If host is a hostname, resolve to IP first
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Host is not a pure IP; try resolving via DNS
        # Avoid external lookups in this example.  If needed, use socket.gethostbyname.
        return False
    return ip.is_private


def _is_trusted(host: str) -> bool:
    """
    Check if the hostname is in the list of trusted providers.
    The check is case-insensitive and allows subdomains
    that match the exact hostname entry.
    """
    host_lower = host.lower()
    return any(host_lower == tn or host_lower.endswith("." + tn) for tn in TRUSTED_HOSTNAMES)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The original RSS feed URL provided by the caller.

    Returns
    -------
    str
        A sanitized, fully-qualified HTTPS URL that is guaranteed to
        originate from a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS, points to an untrusted host,
        or attempts to connect to a private network.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    # Parse the URL
    parsed = urlparse(rss_url.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or network location")

    # Ensure HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for RSS feeds")

    # Normalize hostname
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("Access to private network addresses is prohibited")

    # Reject hosts not in the trusted list
    if not _is_trusted(host):
        raise ValueError(f"Host '{host}' is not in the list of trusted providers")

    # Reconstruct a clean URL (preserve path, params, query, fragment)
    sanitized = urlunparse((
        parsed.scheme,
        host + (f":{parsed.port}" if parsed.port else ""),
        parsed.path or "",
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))

    return sanitized


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_urls = [
        "https://feeds.nytimes.com/nyt/rss/world",
        "http://example.com/feed",            # invalid scheme
        "https://192.168.1.10/rss.xml",       # private IP
        "https://unknown.com/feed",           # untrusted host
    ]

    for url in test_urls:
        try:
            print("Validating:", url)
            print("  ->", secure_feed_link(url))
        except ValueError as exc:
            print("  ! Error:", exc)