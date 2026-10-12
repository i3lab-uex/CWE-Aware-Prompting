import re
from urllib.parse import urlparse, unquote

# List of trusted RSS providers (add more as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "www.reddit.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regex patterns for private and local IP ranges
PRIVATE_IP_PATTERNS = [
    re.compile(r"^10\."),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^127\.0\.0\.1$"),
    re.compile(r"^169\.254\."),  # link-local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private range."""
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(ip):
            return True
    return False

def _is_valid_hostname(hostname: str) -> bool:
    """Basic hostname validation."""
    if not hostname or len(hostname) > 253:
        return False
    # RFC 1123 compliant pattern
    hostname_regex = re.compile(
        r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
    )
    return bool(hostname_regex.match(hostname))

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate an RSS feed URL to ensure it comes from a trusted provider
    and does not target internal/private networks.

    Parameters:
        feed_url (str): The raw URL to sanitize.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is invalid or not from a trusted provider.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    # Parse the URL
    parsed = urlparse(feed_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Decode percent-encoded path to check for hidden IPs
    host = parsed.hostname or ""
    if not _is_valid_hostname(host):
        raise ValueError("Invalid hostname in URL")

    # Reject private IPs
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private IP address")

    # Check against trusted domains
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct a cleaned URL (remove fragments and query params that could be malicious)
    clean_url = f"{parsed.scheme}://{host}"
    if parsed.path:
        clean_url += unquote(parsed.path)

    return clean_url