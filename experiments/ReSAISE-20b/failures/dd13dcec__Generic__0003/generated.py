import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of trusted providers (domain suffixes or exact domains)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com/rss",
    "bbc.co.uk",          # example
    "cnn.com",
}

# Regular expression to detect private IP ranges or localhost
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^localhost$)|                               # localhost hostname
    (^127\.)|(^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)   # private IP ranges
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_host(host: str) -> bool:
    """Return True if host is localhost or a private IP address."""
    # Check for literal IP
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP, check for private patterns in hostname
        return bool(PRIVATE_IP_REGEX.search(host))

def _is_trusted_host(host: str) -> bool:
    """Return True if host matches a trusted provider."""
    # Normalize to lowercase
    host = host.lower()
    for trusted in TRUSTED_PROVIDERS:
        if host == trusted or host.endswith("." + trusted):
            return True
    return False

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that the given RSS feed URL belongs to a trusted provider
    and does not point to an internal or private network resource.

    Parameters
    ----------
    feed_url : str
        The RSS feed URL to validate and sanitize.

    Returns
    -------
    str
        The sanitized, fully-qualified RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an untrusted host,
        or attempts to access a private/internal network resource.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed: ParseResult = urlparse(feed_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {feed_url!r}")

    # Reject non-HTTP(S) schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed.scheme!r}")

    host = parsed.hostname
    if not host:
        raise ValueError(f"Unable to determine hostname from URL: {feed_url!r}")

    # Check for private/internal hosts
    if _is_private_host(host):
        raise ValueError(f"URL points to a private or internal host: {host!r}")

    # Check against trusted providers
    if not _is_trusted_host(host):
        raise ValueError(f"Untrusted feed provider: {host!r}")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = parsed.geturl()
    return sanitized