import re
from urllib.parse import urlparse
import ipaddress

# List of trusted providers (domain names). Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "api.reuters.com",
    "feed.wordpress.com",
    "news.google.com",
}

# Regex to reject URLs that contain IP addresses or private network patterns.
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^|://)                 # start or after scheme
    (?P<ip>
        (?:10\.|172\.(?:1[6-9]|2\d|3[0-1])\.|192\.168\.)   # private ranges
        (?:\d{1,3}\.){2}\d{1,3}
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip_str: str) -> bool:
    """
    Determine if an IP string belongs to a private or reserved range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL originates from a trusted provider
    and does not target an internal network.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes validation checks.

    Raises:
        ValueError: If the URL is malformed, uses an untrusted domain,
                    or targets a private/internal IP address.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that contain an IP address directly in the netloc
    if re.match(PRIVATE_IP_REGEX, url):
        raise ValueError("URL contains a private IP address")

    # Resolve potential IPv4/IPv6 addresses in netloc
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check for IP addresses
    try:
        ip = ipaddress.ip_address(host)
        if _is_private_ip(str(ip)):
            raise ValueError("URL points to a private/internal IP address")
    except ValueError:
        # Not an IP; proceed with domain checks
        pass

    # Normalize the host (lowercase, strip port)
    normalized_host = host.lower()

    # Verify that the hostname ends with a trusted provider domain
    if not any(normalized_host == provider or normalized_host.endswith(f".{provider}") for provider in TRUSTED_PROVIDERS):
        raise ValueError(f"Untrusted feed provider: {normalized_host}")

    return url