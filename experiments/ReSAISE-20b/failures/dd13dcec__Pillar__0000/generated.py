import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted RSS providers (add or remove as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "www.reddit.com",
    "news.google.com",
}

# Regular expression for private IP ranges (RFC 1918, RFC 169.254)
_PRIVATE_IP_PATTERNS = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
]

def _is_private_ip(host: str) -> bool:
    """
    Determine if a host string is a private IP address.
    """
    # Resolve numeric IPs directly
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; check against regex patterns for known private ranges
        return any(p.match(host) for p in _PRIVATE_IP_PATTERNS)

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The RSS feed URL to be sanitized.

    Returns
    -------
    str
        A sanitized and validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL does not belong to trusted providers or attempts to access restricted network URLs.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Only allow HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with empty netloc
    if not parsed.netloc:
        raise ValueError("URL must have a network location (netloc)")

    # Normalize hostname to lowercase
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject private IP addresses or hosts that resolve to them
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # Reject hostnames that are not in the trusted list
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted feed provider: {host}")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized