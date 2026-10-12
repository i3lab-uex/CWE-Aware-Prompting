import re
from urllib.parse import urlparse

# List of approved RSS feed providers (case‑insensitive)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.reuters.com",
    "feed.feedly.com",
}

# Regular expression to reject obvious internal or private addresses
_INTERNAL_PATTERNS = [
    re.compile(r"^(?:localhost|127\.0\.0\.1)$", re.IGNORECASE),
    re.compile(r"^10\.", re.IGNORECASE),          # RFC1918 private network
    re.compile(r"^172\.1[6-9]\.", re.IGNORECASE),
    re.compile(r"^172\.2[0-9]\.", re.IGNORECASE),
    re.compile(r"^172\.3[0-1]\.", re.IGNORECASE),
    re.compile(r"^192\.168\.", re.IGNORECASE),
]

def _is_internal(host: str) -> bool:
    """Return True if the host resolves to a private or local address."""
    for pattern in _INTERNAL_PATTERNS:
        if pattern.match(host):
            return True
    return False

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider
    and does not target private/internal networks.

    Args:
        rss_feed_url: The URL to validate.

    Returns:
        A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider or
                    attempts to access restricted networks.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    parsed = urlparse(rss_feed_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject internal/private addresses
    if _is_internal(host):
        raise ValueError(f"Access to internal network ({host}) is forbidden")

    # Normalize host for comparison
    normalized_host = host.lower()

    if normalized_host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {normalized_host}")

    # Reconstruct the URL to avoid any hidden characters or fragments
    sanitized_url = parsed.geturl()
    return sanitized_url

# Example usage (uncomment to test):
# try:
#     url = filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation failed: {e}")