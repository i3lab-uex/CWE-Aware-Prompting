import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (schemes + hostnames)
TRUSTED_PROVIDERS = {
    ("https", "rss.nytimes.com"),
    ("https", "feeds.feedburner.com"),
    ("https", "www.reddit.com"),
    ("https", "news.google.com"),  # example
}

# Regex to detect internal IP ranges
INTERNAL_IP_REGEX = re.compile(
    r"^("
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(127\.0\.0\.1)"
    r")$"
)


def _is_internal_ip(host: str) -> bool:
    """
    Determine if the given hostname resolves to an internal IP.
    Since DNS resolution may not be desired in this context, we
    perform a quick regex check on the hostname. If it looks like an IP,
    we validate against known private ranges.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a raw IP, skip
        return False


def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be validated.

    Returns
    -------
    str
        A sanitized, validated URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to connect
        to an internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    # Parse the URL
    parsed = urlparse(rss_link)

    # Basic scheme check
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Normalise host (case-insensitive)
    host = parsed.hostname.lower()

    # Reject internal IPs or private ranges
    if _is_internal_ip(host):
        raise ValueError("URL points to a restricted internal network")

    # Check against trusted providers
    if (parsed.scheme.lower(), host) not in TRUSTED_PROVIDERS:
        raise ValueError("URL is not from a trusted provider")

    # Reconstruct the URL to ensure canonical form
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized