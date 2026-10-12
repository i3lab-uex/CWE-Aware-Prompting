import re
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted providers. Extend as needed.
TRUSTED_PROVIDERS = {
    "feeds.nytimes.com",
    "rss.cnn.com",
    "www.reddit.com",
    "news.yahoo.com",
    # add more domains here
}

# Regular expression to detect private IP ranges (RFC1918)
PRIVATE_IP_RE = re.compile(
    r"^(10\.\d{1,3}\.\d{1,3}\.\d{1,3})$|"
    r"^(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$|"
    r"^(192\.168\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address matches a private range."""
    return PRIVATE_IP_RE.match(ip) is not None

def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL that is safe for fetching.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted provider or tries to access a private network.
    """
    # Parse the URL
    parsed = urlparse(feed_address)

    # Basic scheme check (http or https)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IPs (basic check using hostname)
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private network address")

    # Check against trusted providers
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Reconstruct the URL to ensure it has no extraneous components
    sanitized = urlunparse((
        parsed.scheme,
        hostname,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query string if any
        ""   # fragment
    ))
    return sanitized