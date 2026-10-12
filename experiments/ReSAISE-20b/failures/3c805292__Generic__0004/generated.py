import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# List of fully qualified domain names or IP addresses that are considered trusted.
TRUSTED_PROVIDERS = {
    "feeds.nytimes.com",
    "rss.cnn.com",
    "news.google.com",
    "feeds.bbci.co.uk",
    # Add more trusted domains as needed
}

# Regular expression to detect private or local IP ranges.
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|"
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|"
    r"169\.254\.\d{1,3}\.\d{1,3}"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if an IP address string is part of a private network.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; treat as non-private.
        return False

def _normalize_url(parsed: ParseResult) -> str:
    """
    Reconstruct the URL ensuring no fragment or query components are present.
    """
    # Remove fragments and queries for safety
    cleaned = parsed._replace(fragment="", query="")
    return urlunparse(cleaned)

def validate_feed_source(feed_address: str) -> str:
    """
    Validate that the provided RSS feed URL belongs to a trusted provider
    and does not target internal or private network addresses.

    Parameters:
        feed_address (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated URL suitable for fetching.

    Raises:
        ValueError: If the URL is not trusted or points to a restricted network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("Feed address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve hostname to IP addresses (only if host is an IP)
    try:
        ip = ipaddress.ip_address(host)
        # Host is a literal IP address
        if _is_private_ip(str(ip)):
            raise ValueError("Access to private IP addresses is forbidden")
    except ValueError:
        # Host is a domain name; check against trusted providers
        if host.lower() not in TRUSTED_PROVIDERS:
            raise ValueError(f"Untrusted provider: {host}")

    # Sanitize URL (remove fragments and queries)
    sanitized = _normalize_url(parsed)

    return sanitized