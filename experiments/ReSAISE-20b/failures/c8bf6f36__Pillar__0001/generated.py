import re
from urllib.parse import urlparse, urlunparse

# List of approved hostnames for RSS feeds
_TRUSTED_HOSTNAMES = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regex to detect common internal IP patterns
_INTERNAL_IP_RE = re.compile(
    r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.|127\.|169\.254\.)"
)

def _is_internal_ip(host: str) -> bool:
    """
    Simple heuristic to detect if a hostname is an IP address that
    belongs to internal/private ranges.
    """
    try:
        # If host is a dotted IP address
        parts = host.split(".")
        if len(parts) == 4 and all(part.isdigit() for part in parts):
            return bool(_INTERNAL_IP_RE.match(host))
    except Exception:
        pass
    return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The URL to validate.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or points to a restricted internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("RSS link must use http or https scheme")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("RSS link must contain a hostname")

    host = parsed.hostname.lower()
    if _is_internal_ip(host):
        raise ValueError("RSS link points to an internal IP address")

    # Verify host is in the trusted list
    if host not in _TRUSTED_HOSTNAMES:
        raise ValueError(f"RSS link host '{host}' is not an approved provider")

    # Reconstruct the URL to ensure it's normalized
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,  # preserve query string if any
        ""   # fragment
    ))

    return sanitized