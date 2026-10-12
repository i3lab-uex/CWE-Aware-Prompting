import re
from urllib.parse import urlparse, unquote

# List of fully qualified domain names that are considered trusted RSS providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "www.reddit.com",
    "blogspot.com",
    # Add more trusted domains here.
}

# Regular expression to detect private IP ranges.
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 loopback
        (::1)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    return bool(_PRIVATE_IP_REGEX.match(ip))

def _extract_hostname(url: str) -> str:
    """Return the hostname from a URL, normalized to lowercase."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url}")
    # Remove userinfo if present (e.g., http://user:pass@host)
    host = parsed.hostname
    if not host:
        raise ValueError(f"URL missing hostname: {url}")
    return host.lower()

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_feed_url : str
        The URL to validate.

    Returns
    -------
    str
        The sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or attempts to access a private/internal network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    # Unquote percent-encoded characters to avoid hidden IPs
    rss_feed_url = unquote(rss_feed_url)

    host = _extract_hostname(rss_feed_url)

    # Reject if hostname resolves to a private IP
    # NOTE: We avoid DNS resolution for security reasons.
    # Instead, we check if the host is an explicit IP address.
    ip_match = re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host)
    if ip_match and _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Validate against the trusted provider list
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # At this point the URL is considered safe.
    return rss_feed_url