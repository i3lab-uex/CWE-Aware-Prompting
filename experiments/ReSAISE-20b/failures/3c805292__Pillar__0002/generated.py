import re
from urllib.parse import urlparse

# List of trusted providers (domains or sub‑domains)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "news.ycombinator.com",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(                               # start of string
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (192\.168\.\d{1,3}\.\d{1,3})|
        (169\.254\.\d{1,3}\.\d{1,3})|
        (127\.0\.0\.1)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def validate_feed_source(feed_address: str) -> str:
    """
    Validate that a given RSS feed URL originates from a trusted provider
    and does not target an internal network.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original, sanitized URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS, from an untrusted provider,
        or attempts to access a private network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Ensure a network location is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Resolve sub‑domain matching
    host = parsed.hostname.lower()
    if not any(host == trusted or host.endswith("." + trusted) for trusted in TRUSTED_PROVIDERS):
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Detect if the host resolves to a private IP
    # (In production, you'd perform an actual DNS lookup. Here we check the literal host.)
    if _is_private_ip(host):
        raise ValueError("Attempt to access a private IP address is prohibited")

    # Optionally, strip any query parameters that might influence fetching
    sanitized = parsed._replace(query="").geturl()

    return sanitized