#!/usr/bin/env python3
"""
Secure RSS feed URL validator.

The `check_feed_url` function verifies that a given RSS feed URL belongs to
a pre‑approved list of trusted providers and does not point to a private or
internal network address.  It returns the original URL if it passes all checks,
otherwise raises a ValueError.

Author: ChatGPT
"""

import re
import socket
from urllib.parse import urlparse, ParseResult

# --------------------------------------------------------------------------- #
# Configuration: list of trusted hostnames (case‑insensitive)
TRUSTED_HOSTNAMES = {
    "news.yahoo.com",
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "feeds.reuters.com",
    "news.google.com",
}

# Regular expression for matching private IP address ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    return bool(PRIVATE_IP_RE.match(ip))


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IPv4 addresses.

    Raises socket.gaierror if resolution fails.
    """
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None, socket.AF_INET)]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc


def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original, sanitized URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to connect to
        a restricted network area.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed: ParseResult = urlparse(rss_link.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {rss_link!r}")

    # Normalize hostname (lowercase, strip port if present)
    host = parsed.hostname.lower()
    if not host:
        raise ValueError(f"Could not extract hostname from URL: {rss_link!r}")

    # 1. Check against the whitelist
    if host not in TRUSTED_HOSTNAMES:
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # 2. Resolve hostname to IP addresses
    ip_addresses = _resolve_hostname(host)

    # 3. Ensure none of the resolved IPs are private or loopback
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP address {ip} for host '{host}' is in a restricted network range"
            )

    # 4. Reconstruct the URL to ensure no fragments or query parameters that could be malicious
    safe_url = parsed._replace(fragment="", query="").geturl()

    return safe_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         url = check_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")