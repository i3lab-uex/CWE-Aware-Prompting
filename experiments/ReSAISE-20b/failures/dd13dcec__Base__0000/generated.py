import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regex to detect private IP ranges or localhost
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(                       # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |        # 10.0.0.0/8
        172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3} |            # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |        # 127.0.0.0/8
        ::1 |                                  # IPv6 loopback
        169\.254\.\d{1,3}\.\d{1,3}              # Link-local
    )$                      # end of string
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Determine whether a host string is an IP address that belongs to
    a private or loopback range.
    """
    # Direct regex check for common patterns
    if PRIVATE_IP_REGEX.match(host):
        return True

    # Use ipaddress module for more robust checking
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; treat as non‑private
        return False


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw URL provided by a user or upstream component.

    Returns
    -------
    str
        A sanitized, fully qualified URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use HTTP/HTTPS,
        points to a private network address, or belongs to an
        untrusted provider.
    """
    if not feed_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise the netloc (lowercase, remove default ports)
    host = parsed.hostname.lower() if parsed.hostname else ""
    port = parsed.port

    # Reject URLs that resolve to private or loopback IPs
    if _is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP address")

    # Reject URLs with disallowed ports (optional, but can be extended)
    if port and port not in {80, 443}:
        raise ValueError(f"Disallowed port: {port}")

    # Ensure the host is in the trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted provider: {host}")

    # Rebuild the URL to ensure no query parameters or fragments that
    # could alter fetching logic are present.
    safe_parts = (
        parsed.scheme,
        f"{host}:{port}" if port else host,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    sanitized_url = urlunparse(safe_parts)

    return sanitized_url