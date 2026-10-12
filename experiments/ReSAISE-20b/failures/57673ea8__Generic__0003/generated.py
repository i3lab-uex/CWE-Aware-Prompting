import re
from urllib.parse import urlparse
import ipaddress

# List of trusted RSS providers (case‑insensitive)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regex to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10(?:\.\d{1,3}){3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168(?:\.\d{1,3}){2})|
        # localhost
        (?:127(?:\.\d{1,3}){3})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not point to
    any internal or private network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is malformed, not from a trusted domain,
                    or resolves to an internal/private IP address.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")

    # Normalize domain to lowercase
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError(f"URL missing hostname: {url!r}")

    # Check if domain is in the trusted list
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname!r}")

    # Resolve potential numeric IPs
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname):
        if _is_private_ip(hostname):
            raise ValueError(f"URL points to a private IP: {hostname!r}")

    # Additional safety: ensure no embedded private IP in query fragments
    for part in (parsed.query, parsed.fragment):
        if part:
            # Find all IP-like substrings
            for match in re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", part):
                if _is_private_ip(match):
                    raise ValueError(f"Private IP detected in URL component: {match!r}")

    return url