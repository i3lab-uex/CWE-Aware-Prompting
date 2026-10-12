import re
from urllib.parse import urlparse
import ipaddress

# List of trusted provider domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "www.reddit.com",
    "feeds.feedburner.com",
}

# Regex to detect private IP address ranges
_PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[01])\.)"
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host is a private IP address.
    Handles both IPv4 and IPv6.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; could be a hostname
        return False

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and
    does not point to an internal network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is not from a trusted provider or
                    resolves to an internal IP address.
    """
    if not source_url:
        raise ValueError("Source URL must be a non-empty string")

    parsed = urlparse(source_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check for private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private IP address")

    # Check if host is in the list of trusted domains
    host_lower = host.lower()
    if not any(host_lower == t or host_lower.endswith("." + t) for t in _TRUSTED_DOMAINS):
        raise ValueError(f"Host '{host}' is not a trusted RSS provider")

    # Optional: Basic check for internal IP patterns in the URL path/query
    if _PRIVATE_IP_RE.search(parsed.netloc):
        raise ValueError("URL contains internal IP address pattern")

    return source_url