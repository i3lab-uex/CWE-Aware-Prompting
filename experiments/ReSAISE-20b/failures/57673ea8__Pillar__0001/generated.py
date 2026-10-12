import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of trusted RSS feed providers (example domains)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex to detect private IP address ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 link-local and unique local
        (fc00::/7|fe80::/10)
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host is a private IP address.
    Handles both IPv4 and IPv6.
    """
    try:
        # Resolve possible IPv6
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a numeric IP, so assume not private
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that the given RSS feed URL comes from a trusted provider
    and does not target an internal network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is valid and trusted.

    Raises:
        ValueError: If the URL does not belong to a trusted provider
                    or points to an internal/private IP address.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Normalize host (lowercase, strip port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Check for private IP addresses
    if _is_private_ip(hostname):
        raise ValueError(f"URL points to a private IP address: {hostname}")

    # For hostnames, ensure they are in the trusted list
    if hostname.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Additional safety: ensure path is present (RSS feeds typically have a path)
    if not parsed.path or parsed.path == "/":
        raise ValueError("URL must point to a specific RSS feed path")

    # All checks passed; return the original URL
    return url.strip()