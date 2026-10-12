import re
from urllib.parse import urlparse, urlunparse

# Whitelist of trusted RSS feed providers
_TRUSTED_PROVIDERS = {
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "www.reddit.com",
    "news.google.com",   # Google News RSS
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private or loopback IP addresses
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        10\..*|
        172\.(1[6-9]|2[0-9]|3[01])\..*|
        192\.168\..*|
        127\..*|
        ::1$|
        fe80:.*|
        fc00:.*
    )
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host looks like an IP address."""
    return re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host) is not None

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw RSS feed URL supplied by an upstream component.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted provider, or attempts to access
        private/internal network resources.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Ensure we have an explicit scheme
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Normalize the hostname (case-insensitive)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that resolve to private or loopback IP addresses
    if _is_ip_address(host):
        if _PRIVATE_IP_RE.match(host):
            raise ValueError("URL resolves to a private or loopback IP address")
    else:
        # For domain names, reject any that contain disallowed characters
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            raise ValueError("Hostname contains invalid characters")

    # Reject hosts that are not in the trusted provider list
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not a trusted RSS provider")

    # Reconstruct the URL ensuring we strip any userinfo or fragment
    sanitized = urlunparse((
        parsed.scheme.lower(),
        f"{parsed.hostname}{f':{parsed.port}' if parsed.port else ''}",
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query if present
        ""   # fragment removed
    ))

    return sanitized