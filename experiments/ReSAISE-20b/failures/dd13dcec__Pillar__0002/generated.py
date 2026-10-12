import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Trusted RSS providers (add more as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "www.reddit.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\..*|                           # 10.0.0.0 – 10.255.255.255
        172\.(1[6-9]|2\d|3[0-1])\..*|     # 172.16.0.0 – 172.31.255.255
        192\.168\..*|                     # 192.168.0.0 – 192.168.255.255
        169\.254\..*|                     # Link-local addresses
        ::1$ |                            # IPv6 loopback
        fc00:|fd00:                        # Unique local addresses
    )
    .*
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the hostname resolves to a private IP address.
    """
    try:
        # Resolve all addresses for the host
        for addr_info in socket.getaddrinfo(hostname, None):
            ip = addr_info[4][0]
            if PRIVATE_IP_REGEX.match(ip) or ipaddress.ip_address(ip).is_private:
                return True
    except socket.gaierror:
        # If resolution fails, consider it unsafe
        return True
    return False


def _normalize_url(parsed: urlparse) -> str:
    """
    Return a canonical form of the URL.
    """
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = re.sub(r'/+', '/', parsed.path)  # collapse multiple slashes
    return urlunparse((scheme, netloc, path, "", "", ""))


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that `feed_url` is from a trusted RSS provider and does not
    expose internal network resources.

    Parameters:
        feed_url (str): The URL to validate.

    Returns:
        str: A normalized, sanitized URL that can be safely fetched.

    Raises:
        ValueError: If the URL is not trusted or tries to access restricted
                    network addresses.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must have a valid hostname")

    # Reject private or loopback IPs
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or loopback IP address")

    # Check against trusted domains
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not a trusted RSS provider")

    # Return the normalized URL
    return _normalize_url(parsed)