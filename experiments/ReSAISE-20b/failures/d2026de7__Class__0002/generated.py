import re
from urllib.parse import urlparse, urlunparse

# List of approved RSS providers (hostnames only). Extend as needed.
_TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "news.google.com",
    "feeds.feedburner.com",
}

# Regex for private IP ranges (RFC 1918) and localhost
_PRIVATE_IP_RE = re.compile(
    r"^(?:"
    # 10.0.0.0/8
    r"(10(?:\.\d{1,3}){3})|"
    # 172.16.0.0/12
    r"(172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|"
    # 192.168.0.0/16
    r"(192\.168(?:\.\d{1,3}){2})|"
    # 127.0.0.0/8
    r"(127(?:\.\d{1,3}){3})"
    r")$"
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP or localhost."""
    return bool(_PRIVATE_IP_RE.match(host))

def check_rss_address(rss_address: str) -> str:
    """
    Validate that the provided RSS URL belongs to a trusted provider
    and does not target internal/private networks.

    Parameters:
        rss_address (str): The URL to validate.

    Returns:
        str: The sanitized, validated RSS URL.

    Raises:
        ValueError: If the URL is not trusted or attempts to access a private network.
    """
    if not rss_address:
        raise ValueError("RSS address cannot be empty")

    parsed = urlparse(rss_address)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs or localhost
    if _is_private_ip(host):
        raise ValueError("URL points to a private or localhost address")

    # Reject IP addresses (public) that are not in the whitelist
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if host not in _TRUSTED_PROVIDERS:
            raise ValueError("IP-based RSS providers are not trusted")

    # Ensure the host is in the whitelist
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to normalize it (e.g., remove fragments)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment removed for safety
    ))
    return sanitized