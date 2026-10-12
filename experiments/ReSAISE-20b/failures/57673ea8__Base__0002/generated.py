import re
from urllib.parse import urlparse, unquote
import ipaddress

# Trusted external providers (add more as needed)
_TRUSTED_DOMAINS = {
    "feeds.reuters.com",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
}

# Regular expression to detect IPv4 or IPv6 addresses in a hostname
_IP_REGEX = re.compile(r"""
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )
""", re.VERBOSE)


def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the hostname is a private IP address.
    Handles both IPv4 and IPv6. Raises ValueError if the hostname
    cannot be parsed as an IP address.
    """
    try:
        # ipaddress will raise ValueError if hostname is not an IP
        return bool(ipaddress.ip_address(hostname).is_private)
    except ValueError:
        return False


def _hostname_is_trusted(hostname: str) -> bool:
    """
    Determine if a hostname is trusted. Accepts domain names or IP addresses.
    For domain names, checks against the whitelist.
    For IP addresses, ensures they are not private and optionally add to a
    whitelist of public IPs if required.
    """
    # Normalize hostname (remove trailing dot, convert to lowercase)
    hostname = hostname.rstrip(".").lower()

    # If the hostname is an IP address, ensure it isn't private
    if _IP_REGEX.fullmatch(hostname):
        return not _is_private_ip(hostname)

    # For domain names, check against the whitelist
    return hostname in _TRUSTED_DOMAINS


def validate_feed_url(url: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL does not use http/https, points to a private IP,
        or is not from an authenticated provider.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(url)

    # Only http/https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Decode percent-encoded characters in the hostname
    hostname = unquote(parsed.hostname or "")

    # Reject private IP addresses and localhost
    if _is_private_ip(hostname) or hostname in {"localhost", "127.0.0.1"}:
        raise ValueError("URL points to a private or local network address")

    # Verify that the hostname is trusted
    if not _hostname_is_trusted(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the trusted list")

    # All checks passed; return the original URL
    return url