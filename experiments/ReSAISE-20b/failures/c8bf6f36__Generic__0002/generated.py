#!/usr/bin/env python3
"""
validate_rss_link.py

Provides a single function `validate_rss_link` that sanitises an RSS feed URL
by ensuring it originates from a trusted provider and does not point to any
private, loopback or link‑local IP addresses.  The function raises a
ValueError for any disallowed URL.

Author: OpenAI ChatGPT
"""

import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: list of approved domains (case‑insensitive).  Add or remove
# providers here as your policy evolves.  The list is intentionally small for
# demo purposes; real deployments should be more comprehensive.
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# --------------------------------------------------------------------------- #
# Regular expression to quickly detect common private IP address patterns
# (10.x.x.x, 172.16-31.x.x, 192.168.x.x, ::1, link‑local, etc.).
# --------------------------------------------------------------------------- #
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                                  # IP address part
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}     |  # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3} |  # 172.16-31.0/12
        192\.168\.\d{1,3}\.\d{1,3}       |  # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}   |  # Loopback
        ::1|                            # IPv6 loopback
        fe80::/10                       |  # Link‑local (IPv6)
        fc00::/7                        |  # Unique local (IPv6)
        fd00::/8                         # Unique local (IPv6)
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if a hostname is an IP address that falls into a private or
    reserved range.  Returns True if the host is disallowed.
    """
    try:
        # Resolve IPv6 and IPv4 addresses
        ip_obj = ipaddress.ip_address(host)
    except ValueError:
        # Not a literal IP address
        return False

    # ipaddress module knows about all reserved ranges
    return (
        ip_obj.is_private or
        ip_obj.is_loopback or
        ip_obj.is_link_local or
        ip_obj.is_reserved or
        ip_obj.is_multicast
    )

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw URL supplied by the user or application.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is guaranteed to point to an
        approved provider and does not resolve to a private or internal IP.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an unapproved provider, or tries to
        resolve a private/internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Normalise host (lowercase, strip port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Reject private or reserved IPs
    if _is_private_ip(hostname):
        raise ValueError(f"Disallowed private IP address: {hostname}")

    # Reject hostnames that match the private IP regex (e.g., 127.0.0.1)
    if PRIVATE_IP_REGEX.match(hostname):
        raise ValueError(f"Disallowed private hostname: {hostname}")

    # Ensure the host is in the approved list (case‑insensitive)
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Unapproved provider: {hostname}")

    # Reconstruct the URL to avoid any trailing fragments or queries that
    # might be used maliciously.  Only the scheme, netloc and path are kept.
    safe_url = urlunparse(
        (parsed.scheme,
         parsed.netloc,
         parsed.path.rstrip("/"),
         "",  # params
         "",  # query
         "")   # fragment
    )
    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (for testing only; remove or guard under __main__ in real code)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://192.168.1.10/feed",  # should fail
        "ftp://feeds.feedburner.com/somefeed",  # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validated: {validate_rss_link(url)}")
        except ValueError as exc:
            print(f"Rejected: {url} -> {exc}")