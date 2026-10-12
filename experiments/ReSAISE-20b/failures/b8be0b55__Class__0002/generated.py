import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A whitelist of trusted external RSS providers (case‑insensitive)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to match common internal IP address patterns
_INTERNAL_IP_REGEX = re.compile(
    r"""
    (^127\.0\.0\.1$)|                                 # loopback
    (^(10|172\.16|192\.168)\.)|                       # private networks
    (^169\.254\.)|
    (^::1$)|                                          # IPv6 loopback
    (^fc00:|^fd00:)                                    # IPv6 unique local addresses
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_internal_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _is_internal_hostname(hostname: str) -> bool:
    """Check if a hostname resolves to an internal IP address."""
    # Resolve the hostname; we only perform a simple check for local addresses.
    # In production, consider using a DNS resolver with caching and timeout.
    try:
        import socket
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if _is_internal_ip(ip):
                return True
    except Exception:
        # If DNS resolution fails, treat it as unsafe to be conservative.
        return True
    return False

def clean_feed_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers and
    ensure it does not point to internal network addresses.

    Parameters:
        rss_link (str): The RSS feed URL to sanitize.

    Returns:
        str: The sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not trusted or points to an internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP(S) schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that resolve to internal IP addresses
    if _is_internal_hostname(hostname):
        raise ValueError("URL resolves to an internal network address")

    # Check against the trusted domain whitelist (case‑insensitive)
    if hostname.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the trusted provider list")

    # Reconstruct the URL to ensure canonical form (e.g., lowercasing scheme and host)
    sanitized = urlunparse((
        parsed.scheme.lower(),
        hostname.lower() + (f":{parsed.port}" if parsed.port else ""),
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return sanitized

# Example usage (uncomment to test):
# try:
#     print(clean_feed_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
# except ValueError as e:
#     print(f"Invalid feed URL: {e}")