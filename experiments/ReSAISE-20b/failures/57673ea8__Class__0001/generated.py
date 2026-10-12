#!/usr/bin/env python3
"""
Utility to validate RSS feed URLs against a whitelist of trusted providers.
The function ensures that the URL:
* uses http or https,
* resolves to a public IP address (not private, loopback, link-local, etc.),
* and its hostname is in the predefined whitelist.

This protects against accidental internal network access (CWE-441).
"""

import re
import socket
from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# Whitelist of trusted feed providers (hostnames or domain patterns)
TRUSTED_HOSTS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",          # Google News RSS
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "reuters.com",
}

# Compile regex for wildcard patterns (e.g., *.feedburner.com)
WILDCARD_PATTERNS = [re.compile(r"^.*\.feedburner\.com$")]


def _is_public_ip(ip: str) -> bool:
    """Return True if the IP is not in a private or reserved range."""
    try:
        ip_obj = ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    if isinstance(ip_obj, (IPv4Address, IPv6Address)):
        # Exclude private, loopback, link-local, multicast, and reserved addresses
        return not (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
        )
    return False


def _is_trusted_host(host: str) -> bool:
    """Check if the hostname matches a trusted provider."""
    host = host.lower()
    if host in TRUSTED_HOSTS:
        return True
    for pattern in WILDCARD_PATTERNS:
        if pattern.match(host):
            return True
    return False


def validate_feed_url(url: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a non-public IP, or its host is not trusted.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Resolve the host to all IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    # Ensure at least one IP is public
    if not any(_is_public_ip(addr[4][0]) for addr in addr_info):
        raise ValueError("Hostname resolves only to private or reserved IP addresses")

    # Check against the whitelist
    if not _is_trusted_host(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not a trusted provider")

    # All checks passed
    return url


# Example usage (uncomment for quick testing)
# if __name__ == "__main__":
#     test_urls = [
#         "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
#         "http://localhost/feed",
#         "https://untrusted.com/rss",
#     ]
#     for u in test_urls:
#         try:
#             print(validate_feed_url(u))
#         except ValueError as e:
#             print(f"Invalid: {u} -> {e}")