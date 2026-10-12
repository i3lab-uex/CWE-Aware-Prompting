#!/usr/bin/env python3
"""
Utility to sanitize RSS feed URLs before fetching them.

This module protects against Server‑Side Request Forgery (CWE‑918) by:
* Ensuring the URL uses a safe scheme (`http` or `https`).
* Rejecting URLs that resolve to private IP ranges, loopback addresses,
  or other restricted networks.
* Accepting only URLs whose hostname is in a whitelist of trusted RSS
  providers (e.g. `rss.nytimes.com`, `feeds.feedburner.com`).

Author: OpenAI ChatGPT
"""

import re
import ipaddress
from urllib.parse import urlparse, urlunparse


# --------------------------------------------------------------------------- #
# Configuration:  Whitelist of trusted hostnames (case‑insensitive)
# --------------------------------------------------------------------------- #
TRUSTED_HOSTS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.npr.org",
    # Add more trusted providers here
}

# --------------------------------------------------------------------------- #
# Regular expression to detect private IP ranges, localhost and other
# restricted addresses in dotted‑decimal notation.
# --------------------------------------------------------------------------- #
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                                     # Start of non‑capturing group
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}        # 10.0.0.0/8
      | 172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}  # 172.16.0.0/12
      | 192\.168\.\d{1,3}\.\d{1,3}          # 192.168.0.0/16
      | 127\.\d{1,3}\.\d{1,3}\.\d{1,3}      # 127.0.0.0/8 (loopback)
      | 169\.254\.\d{1,3}\.\d{1,3}          # Link‑local
      | 0\.\d{1,3}\.\d{1,3}\.\d{1,3}        # 0.0.0.0
      | 255\.255\.255\.255                 # Broadcast
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Determine whether a hostname resolves to a private IP address.
    The function performs two checks:
      1. If the host is an explicit dotted‑decimal IP, it is validated
         against a regex for private ranges.
      2. If the host is a hostname, it attempts to resolve it and
         checks whether any resolved address falls into a private range.
    """
    # Check explicit IP string
    if PRIVATE_IP_RE.match(host):
        return True

    try:
        # Resolve the host to IP addresses
        for ip_str in ipaddress.ip_address(host):
            pass  # not a string; skip
    except ValueError:
        # Not an IP literal, attempt DNS resolution
        try:
            import socket

            for ip in socket.getaddrinfo(host, None):
                addr = ip[4][0]
                if _is_private_ip(addr):
                    return True
        except Exception:
            # If DNS resolution fails, treat as unsafe to err on the side of caution
            return True

    return False


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw user‑supplied RSS feed URL.

    Returns
    -------
    str
        A sanitized, validated URL that is safe to fetch.

    Raises
    ------
    ValueError
        If the URL does not use a safe scheme, resolves to a private IP,
        or is not from one of the trusted providers.
    """
    if not feed_url:
        raise ValueError("Feed URL must not be empty")

    parsed = urlparse(feed_url)

    # 1. Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Hostname extraction
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 3. Reject IP addresses and private networks
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            raise ValueError("URL resolves to a private or reserved IP address")
    except ValueError:
        # Not an IP literal; ensure hostname does not resolve to a private IP
        if _is_private_ip(host):
            raise ValueError("Hostname resolves to a private or restricted IP")

    # 4. Whitelist check (case‑insensitive)
    if host.lower() not in {h.lower() for h in TRUSTED_HOSTS}:
        raise ValueError(f"Hostname '{host}' is not a trusted RSS provider")

    # 5. Re‑construct the URL to ensure no accidental query or fragment
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            host,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost:8000/feed.xml",
        "https://example.com/feed",
    ]

    for url in test_urls:
        try:
            print("Sanitized:", sanitize_feed_url(url))
        except ValueError as e:
            print(f"Rejected '{url}': {e}")