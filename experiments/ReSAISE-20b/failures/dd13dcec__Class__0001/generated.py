import re
from urllib.parse import urlparse, urlunparse

# A set of trusted RSS feed providers.  Add or remove as needed.
_TRUSTED_PROVIDERS = {
    "feeds.npr.org",
    "rss.cnn.com",
    "news.google.com",
    "rss.bbc.co.uk",
    "feeds.feedburner.com",
    "news.yahoo.com",
}

# Regex for private IP ranges (CWE-441 prevention)
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:  # start of IP
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |
        (?:192\.168\.\d{1,3}\.\d{1,3}) |
        (?:127\.0\.0\.1)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    return bool(_PRIVATE_IP_REGEX.match(ip))

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and return a sanitized RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw RSS feed URL supplied by the caller.

    Returns
    -------
    str
        A normalized, validated RSS feed URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted provider or attempts to access
        a restricted network address.
    """
    if not feed_url:
        raise ValueError("feed_url must be a non-empty string")

    # Parse the URL
    parsed = urlparse(feed_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise hostname (case-insensitive)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or loopback IP addresses
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname):
        if _is_private_ip(hostname):
            raise ValueError("URL points to a private network address")

    # Ensure the hostname ends with one of our trusted domains
    if not any(hostname.lower().endswith(tld) for tld in _TRUSTED_PROVIDERS):
        raise ValueError(f"Untrusted feed provider: {hostname}")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc.lower(), parsed.path or "/", "", "", "")
    )

    return sanitized