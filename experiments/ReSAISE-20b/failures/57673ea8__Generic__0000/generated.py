import re
from urllib.parse import urlparse

# List of trusted providers (domain names). Subdomains are allowed.
TRUSTED_DOMAINS = [
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "blogspot.com",          # example of a common RSS provider
    "wordpress.com",
]

# Regular expression for detecting private IP addresses and localhost.
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.              # 10.0.0.0/8
     |^172\.(1[6-9]|2[0-9]|3[01])\.   # 172.16.0.0/12
     |^192\.168\.)      # 192.168.0.0/16
    """,
    re.VERBOSE,
)

LOCALHOST_REGEX = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)


def _is_private_host(host: str) -> bool:
    """
    Determine whether the given host is a private IP or localhost.
    """
    # Strip port if present
    host = host.split(":")[0]
    # IPv6 loopback
    if LOCALHOST_REGEX.match(host):
        return True

    # Detect numeric IP addresses
    ip_parts = host.split(".")
    if len(ip_parts) == 4 and all(part.isdigit() for part in ip_parts):
        if PRIVATE_IP_REGEX.match(host):
            return True
    return False


def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the domain ends with one of the trusted domains.
    """
    for trusted in TRUSTED_DOMAINS:
        if domain.lower().endswith(trusted):
            return True
    return False


def validate_feed_url(url: str) -> str:
    """
    Validate an RSS feed URL ensuring it comes from a trusted provider and does not
    target private/internal network addresses.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is malformed, points to a private/internal address,
                    or does not belong to a trusted provider.
    """
    if not url:
        raise ValueError("URL must be non-empty")

    parsed = urlparse(url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal/private addresses
    if _is_private_host(host):
        raise ValueError(f"URL points to a private or internal host: {host}")

    # Verify that the domain is trusted
    if not _is_trusted_domain(host):
        raise ValueError(f"Host {host} is not a trusted RSS provider")

    return url