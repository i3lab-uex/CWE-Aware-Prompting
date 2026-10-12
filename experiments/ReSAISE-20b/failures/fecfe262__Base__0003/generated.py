import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelist of approved RSS providers (sub‑domains allowed)
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",          # example
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                                 # IPv4
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}
    )
    |
    (?:                                 # IPv6
        fe80::|                         # link‑local
        fc00:|fd00:                      # unique local
    )
    .*
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def _resolve_host(hostname: str):
    """Resolve hostname to a list of IP addresses."""
    try:
        return socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate an RSS feed URL, ensuring it points to a trusted provider
    and does not resolve to private/internal IP addresses.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized, trusted feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider,
                    or if it resolves to a private IP address.
    """
    # Basic URL parsing
    parsed = urlparse(rss_feed_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against the approved domain list (case‑insensitive)
    if not any(hostname.lower() == d or hostname.lower().endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Hostname '{hostname}' is not an approved RSS provider")

    # Resolve the hostname to IP addresses and check for private ranges
    addrinfo = _resolve_host(hostname)
    if not addrinfo:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address: {ip}")

    # Reconstruct the URL with normalized components
    sanitized = urlunparse(
        (
            parsed.scheme,
            f"{hostname}:{parsed.port}" if parsed.port else hostname,
            parsed.path or "/",
            "",  # params
            parsed.query,  # preserve query string if any
            "",  # fragment
        )
    )

    return sanitized