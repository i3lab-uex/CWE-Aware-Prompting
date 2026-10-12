import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogfeed.example.com",  # example trusted domain
}

# Regular expression to detect IPv4 or IPv6 addresses in a hostname
IP_REGEX = re.compile(
    r"""
    ^(?:
        (?:
            # IPv4
            (?:\d{1,3}\.){3}\d{1,3}
        )
    |
        \[
            # IPv6
            [0-9a-fA-F:]+
        \]
    )$
    """,
    re.VERBOSE,
)

def _is_internal_ip(ip: str) -> bool:
    """
    Determine if an IP address is internal (private, loopback, link-local, etc.).
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def clean_feed_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL and ensure it originates from a trusted provider.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL that needs sanitization.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, does not belong to a trusted provider,
        or resolves to an internal network address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject explicit IP addresses (internal or external)
    if IP_REGEX.match(host):
        if _is_internal_ip(host.lstrip("[").rstrip("]")):
            raise ValueError(f"URL points to an internal IP address: {host}")
        # If it's a public IP, reject it as we only allow domain names
        raise ValueError(f"Public IP addresses are not allowed: {host}")

    # Normalize the hostname (lowercase)
    host = host.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it remains unchanged
    cleaned = urlunparse(parsed)
    return cleaned