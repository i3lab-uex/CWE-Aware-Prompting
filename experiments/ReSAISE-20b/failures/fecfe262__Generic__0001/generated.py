import re
from urllib.parse import urlparse, urlunparse

# A minimal whitelist of trusted RSS providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.reuters.com",
    "feeds.feedburner.com",
}

# Ensure the URL uses HTTPS and is from a trusted provider.
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
        The original URL if it is trusted and secure.

    Raises
    ------
    ValueError
        If the URL does not use HTTPS or is not from a trusted provider,
        or if it attempts to access restricted internal networks.
    """
    # Basic validation: non-empty string
    if not isinstance(rss_feed_url, str) or not rss_feed_url.strip():
        raise ValueError("RSS feed URL must be a non-empty string")

    parsed = urlparse(rss_feed_url.strip())

    # Reject schemes other than https
    if parsed.scheme.lower() != "https":
        raise ValueError("RSS feed URL must use HTTPS")

    # Reject URLs that target private IP ranges or localhost
    private_ip_pattern = re.compile(
        r"""
        ^(?:
            (?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
            192\.168\.\d{1,3}\.\d{1,3}|
            172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}
        )$
        """,
        re.VERBOSE,
    )
    if private_ip_pattern.match(parsed.hostname or ""):
        raise ValueError("RSS feed URL points to a restricted internal network")

    # Ensure the hostname is in the whitelist
    if parsed.hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {parsed.hostname}")

    # Reconstruct the URL to enforce canonical form
    sanitized = urlunparse(parsed._replace(path=parsed.path or "/", params="", query="", fragment=""))
    return sanitized