import re
from urllib.parse import urlparse, unquote
import ipaddress

# Trusted external providers – adjust as needed
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",  # example
}

# Regex for common private IP ranges (IPv4 and IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"""
    (
        # 10.0.0.0/8
        (?:10(?:\.\d{1,3}){3})
      |
        # 172.16.0.0/12
        (?:172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})
      |
        # 192.168.0.0/16
        (?:192\.168(?:\.\d{1,3}){2})
      |
        # 127.0.0.0/8 (loopback)
        (?:127(?:\.\d{1,3}){3})
      |
        # IPv6 unique local addresses
        (?:fc00::/7)
      |
        # IPv6 loopback
        (::1)
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address or resolves to one."""
    try:
        # Direct numeric check
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a numeric IP – check against regex (for IPv6 literals)
        return bool(PRIVATE_IP_REGEX.search(host))

def _normalize_hostname(host: str) -> str:
    """Lowercase and strip port if present."""
    host = host.lower()
    return host.split(":")[0]

def check_rss_source(source_url: str) -> str:
    """
    Validate that the RSS feed URL comes from a trusted provider and
    does not point to an internal/private network address.

    Args:
        source_url: The URL of the RSS feed to validate.

    Returns:
        The original URL if it is valid and trusted.

    Raises:
        ValueError: If the URL is not from a trusted provider or points
                    to an internal/private network.
    """
    if not source_url:
        raise ValueError("Source URL must be non-empty")

    parsed = urlparse(source_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Normalize hostname
    host = _normalize_hostname(parsed.hostname or "")

    if not host:
        raise ValueError("URL must contain a hostname")

    # Check for internal/private IPs or domains
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Check against trusted domains
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not in the list of trusted providers")

    # All checks passed – return the original URL
    return source_url

# Example usage (commented out for production code)
# try:
#     valid_url = check_rss_source("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Valid URL: {valid_url}")
# except ValueError as e:
#     print(f"Invalid RSS source: {e}")