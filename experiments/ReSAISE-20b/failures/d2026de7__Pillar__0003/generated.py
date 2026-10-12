import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal whitelist of trusted RSS providers.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
    "medium.com",          # Medium RSS feeds
}

# Regular expression to detect IP addresses in the hostname part.
_IP_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given string is a private IP address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private
    except ValueError:
        # Not a valid IP address.
        return False

def _is_trusted_hostname(hostname: str) -> bool:
    """
    Determine if the hostname is part of the trusted domain list
    or a sub‑domain thereof.
    """
    # Normalize to lower case.
    hostname = hostname.lower()

    if _IP_REGEX.match(hostname):
        # Reject plain IP addresses that are private.
        return not _is_private_ip(hostname)

    for domain in _TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False

def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_address : str
        The URL to validate.

    Returns
    -------
    str
        The sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL does not use a safe scheme, points to an untrusted domain,
        or attempts to access a private/internal network.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Only allow http or https schemes.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # The hostname must be present.
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject any host that resolves to a private IP.
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private IP address")

    # Ensure the hostname is from a trusted provider.
    if not _is_trusted_hostname(parsed.hostname):
        raise ValueError(f"Untrusted RSS provider: {parsed.hostname}")

    # Reconstruct the URL to ensure it is properly formatted.
    sanitized = urlunparse(parsed)
    return sanitized