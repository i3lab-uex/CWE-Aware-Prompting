import re
from urllib.parse import urlparse, ParseResult

# List of trusted providers (add more as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "www.reddit.com",  # example
}

# Regex to detect private IP ranges and localhost
_PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if ip is a private or reserved address."""
    return bool(_PRIVATE_IP_RE.match(ip))

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that the provided feed URL is from a trusted provider
    and does not point to internal or private networks.

    Parameters
    ----------
    feed_url : str
        The RSS feed URL to be sanitized.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is not trusted, uses an unsupported scheme,
        or points to a private/internal address.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed: ParseResult = urlparse(feed_url)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # Reject private IPs or localhost
    if _is_private_ip(host) or host in ("localhost", "127.0.0.1"):
        raise ValueError("URL points to a private or local network address")

    # Check against trusted domain list
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted feed provider: {host}")

    # Reconstruct the URL to ensure no path traversal or query injection
    safe_url = parsed.geturl()
    return safe_url

# Example usage (commented out)
# try:
#     url = sanitize_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Sanitized URL: {url}")
# except ValueError as e:
#     print(f"Invalid feed URL: {e}")