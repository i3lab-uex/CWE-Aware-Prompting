import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (domain names)
_TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogspot.com",
    "medium.com",
    "news.google.com",
}

# Regex to detect IP addresses in the hostname part
_IP_REGEX = re.compile(r"""
    ^(?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6 (simple form)
        \[[0-9a-fA-F:]+\]
    )$
""", re.VERBOSE)


def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP string is a private or reserved address.
    Handles both IPv4 and IPv6. Raises ValueError if the string is not a
    valid IP address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL against a list of trusted providers and
    reject any URLs that point to private/internal networks.

    Args:
        rss_url: The raw RSS feed URL supplied by the user.

    Returns:
        A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or
                    attempts to connect to a restricted network area.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    # Parse the URL
    parsed = urlparse(rss_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses in private or reserved ranges
    if _IP_REGEX.match(host):
        # Strip brackets for IPv6 if present
        ip = host.strip("[]")
        if _is_private_ip(ip):
            raise ValueError(f"URL points to a private network: {host}")

    # Ensure host is in the trusted list (case-insensitive)
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host}")

    # Reconstruct the URL to ensure no accidental fragments or
    # other components that might be malicious.
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",          # params
        parsed.query,  # keep query parameters as they might be needed
        "",          # fragment removed
    ))

    return sanitized