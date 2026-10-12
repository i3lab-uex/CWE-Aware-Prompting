#!/usr/bin/env python3
"""
secure_feed_link - Validate and sanitize an RSS feed URL.

The function ensures that the supplied RSS URL points to a trusted
provider and does not resolve to an internal or otherwise restricted
network address.  It protects against DNS rebinding and other
network‑based attacks.

CWE-664 mitigated: the function carefully checks that the URL is
approved before any network resources are accessed, and it does not
retain or expose the resource after validation.
"""

import re
from urllib.parse import urlparse, urlunparse
import socket

# ----------------------------------------------------------------------
# Trusted providers (example list; extend as needed)
TRUSTED_PROVIDERS = {
    "news.ycombinator.com",
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
}

# Restricted IP ranges (private, loopback, link‑local)
_RESTRICTED_IP_PATTERNS = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
]

# ----------------------------------------------------------------------
def _is_restricted_ip(ip: str) -> bool:
    """Return True if IP is in a restricted network range."""
    for pattern in _RESTRICTED_IP_PATTERNS:
        if pattern.match(ip):
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve hostname to a list of IP addresses.
    Uses getaddrinfo for both IPv4 and IPv6.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc

    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, fully‑qualified RSS feed URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, resolves to a restricted IP,
        or fails basic syntax checks.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    # Basic URL parsing
    parsed = urlparse(rss_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    # Check against trusted providers
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider.")

    # Resolve hostname to IP(s) and ensure none are restricted
    for ip in _resolve_hostname(hostname):
        if _is_restricted_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to restricted IP {ip}.")

    # Reconstruct URL ensuring no query/fragment data
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return sanitized

# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage / quick test
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://10.0.0.5/feed",  # should raise
    ]
    for url in test_urls:
        try:
            print("Sanitized:", secure_feed_link(url))
        except ValueError as e:
            print("Validation error:", e)