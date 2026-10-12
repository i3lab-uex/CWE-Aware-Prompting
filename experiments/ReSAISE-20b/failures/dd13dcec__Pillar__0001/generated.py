import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Trusted RSS feed domains (add more as needed)
_TRUSTED_DOMAINS = {
    "news.google.com",
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "api.espn.com",
    "rss.cnn.com",
}

# Regular expression to detect private or loopback IP addresses
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)  # private IPv4
    |^127\.0\.0\.1$                                 # localhost
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if host is a private IP address or localhost.
    Handles both IPv4 and IPv6 addresses.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, return False
        return False

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that a given RSS feed URL belongs to a trusted provider
    and does not expose internal network resources.

    Parameters:
        feed_url (str): The RSS feed URL to sanitize.

    Returns:
        str: A sanitized and validated RSS feed URL.

    Raises:
        ValueError: If the URL is not HTTPS, does not belong to a trusted
                    provider, or attempts to access restricted network URLs.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    # Parse the URL
    parsed = urlparse(feed_url.strip())

    # Must use HTTPS or HTTP scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses or private networks
    host = parsed.hostname.lower()
    if _is_private_ip(host) or _PRIVATE_IP_RE.match(host):
        raise ValueError("URL points to a private or restricted network address")

    # Reject subdomains not explicitly trusted
    if host not in _TRUSTED_DOMAINS:
        # Allow subdomains of trusted domains (e.g., foo.rss.nytimes.com)
        if not any(host.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
            raise ValueError("URL is not from a trusted provider")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized