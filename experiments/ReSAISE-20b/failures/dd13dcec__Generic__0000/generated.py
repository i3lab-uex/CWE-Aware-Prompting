import re
from urllib.parse import urlparse, urlunparse

# List of trusted RSS providers (example entries)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.ycombinator.com",
    "bbc.co.uk",
    "cnn.com",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    return PRIVATE_IP_RE.match(host) is not None

def _is_trusted_domain(host: str) -> bool:
    """Return True if host is in the trusted domain list."""
    # Normalize subdomains by checking the effective top-level domain
    return any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS)

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
        A sanitized and validated RSS feed URL (scheme + netloc + path).

    Raises
    ------
    ValueError
        If the URL is not HTTP/HTTPS, points to a private network,
        or does not belong to a trusted provider.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # Reject localhost
    if host in ("localhost", "127.0.0.1"):
        raise ValueError("URL points to localhost")

    # Validate against trusted providers
    if not _is_trusted_domain(host):
        raise ValueError(f"Untrusted provider: {host}")

    # Reconstruct the URL to ensure no fragments or query parameters
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
    )
    return sanitized