import re
from urllib.parse import urlparse, urlunparse

# List of allowed RSS feed providers (netlocs)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
}

# Regex to detect private or local IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                      # start non-capturing group
        10\.                 # 10.0.0.0 – 10.255.255.255
        \d{1,3}\.\d{1,3}\.\d{1,3}
        |
        172\.(?:1[6-9]|2\d|3[0-1])\.   # 172.16.0.0 – 172.31.255.255
        \d{1,3}\.\d{1,3}
        |
        192\.168\.\d{1,3}\.\d{1,3}     # 192.168.0.0 – 192.168.255.255
        |
        127\.0\.0\.1                   # loopback
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or local."""
    return bool(PRIVATE_IP_RE.match(ip))

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized and validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted provider or attempts
        to access restricted network addresses.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Enforce https or http only
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http or https URLs are allowed")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(parsed.netloc.split(":")[0]):
        raise ValueError("URL resolves to a private IP address")

    # Validate against trusted providers
    host = parsed.hostname.lower()
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted feed provider: {host}")

    # Rebuild URL to ensure no unexpected fragments or parameters
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized