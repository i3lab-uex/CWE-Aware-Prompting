import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# ------------------------------------------------------------------
# Trusted RSS feed providers (domain names or host patterns)
# ------------------------------------------------------------------
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private IP address patterns
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # Direct IP check
        ipaddress.ip_address(host)
        return host in (
            "127.0.0.1",
            "localhost",
        ) or _PRIVATE_IP_REGEX.match(host) is not None
    except ValueError:
        # Not an IP, fallback to regex for IPv4-like strings
        return _PRIVATE_IP_REGEX.match(host) is not None

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL by ensuring it comes from a trusted provider
    and does not point to internal or private network addresses.

    Parameters:
        rss_link (str): The RSS feed URL to validate and sanitize.

    Returns:
        str: The sanitized, trusted RSS feed URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or points to
                    an internal/private network address.
    """
    if not rss_link:
        raise ValueError("RSS link cannot be empty")

    # Parse the URL and validate scheme
    parsed: ParseResult = urlparse(rss_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs or localhost
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private or local network address: {host}")

    # Ensure the host matches one of the trusted providers
    if not any(host == provider or host.endswith("." + provider) for provider in TRUSTED_PROVIDERS):
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure it's normalized
    sanitized_url = parsed.geturl()
    return sanitized_url