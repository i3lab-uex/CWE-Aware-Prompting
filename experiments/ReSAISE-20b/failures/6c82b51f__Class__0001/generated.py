import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# List of fully qualified domain names that are considered trusted providers.
TRUSTED_DOMAINS = {
    "feeds.nytimes.com",
    "rss.cnn.com",
    "news.yahoo.com",
    "feeds.feedburner.com",
    "www.reuters.com",
}

# Regular expression to detect private IP ranges (RFC 1918 and loopback)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2\d|3[0-1])\.)"
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host resolves to a private IP address.
    """
    try:
        # Resolve host to all possible addresses
        for addr_info in socket.getaddrinfo(host, None):
            ip = addr_info[4][0]
            if PRIVATE_IP_REGEX.match(ip) or ipaddress.ip_address(ip).is_private:
                return True
    except Exception:
        # If resolution fails we cannot confirm; treat as unsafe
        return True
    return False

def _sanitize_url(parsed: ParseResult) -> str:
    """
    Return a canonical form of the URL: scheme, netloc (lowercase), path.
    """
    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Remove fragments and query parameters for safety
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc.lower(),
        path=parsed.path or "/",
        params="",
        query="",
        fragment=""
    )
    return urlunparse(sanitized)

def check_feed_url(rss_link: str) -> str:
    """
    Validate that the provided RSS link is from a trusted provider and does not
    point to an internal or private network.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, canonical form of the valid URL.

    Raises:
        ValueError: If the URL is not trusted or points to a private network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Normalize host to compare with trusted list
    host = parsed.hostname.lower()
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Prevent requests to private or internal IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or restricted network")

    return _sanitize_url(parsed)