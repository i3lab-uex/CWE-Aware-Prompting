import re
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted providers – extend as needed
TRUSTED_PROVIDERS = {
    "news.ycombinator.com",
    "feeds.reuters.com",
    "rss.nytimes.com",
    "blog.feedspot.com",
    "news.google.com",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def validate_feed_source(feed_address: str) -> str:
    """
    Validate that the provided RSS feed URL comes from a trusted provider
    and does not point to an internal/private network.

    Parameters:
        feed_address (str): The RSS feed URL to validate.

    Returns:
        str: The sanitized, validated URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or
                    attempts to access a private network.
    """
    # Basic URL parsing
    parsed = urlparse(feed_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {feed_address!r}")

    host = parsed.hostname.lower()

    # Reject URLs that resolve to private IPs (prevents SSRF)
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private network: {feed_address!r}")

    # Ensure host is in the trusted list
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host!r}")

    # Reconstruct a clean URL (remove fragments, query params not needed for RSS)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        '',          # params
        '',          # query
        ''           # fragment
    ))

    return sanitized