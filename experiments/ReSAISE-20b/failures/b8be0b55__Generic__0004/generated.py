import socket
import ipaddress
from urllib.parse import urlparse, unquote

# List of trusted provider hostnames (case‑insensitive)
TRUSTED_HOSTNAMES = {
    'news.google.com',
    'rss.cnn.com',
    'feeds.reuters.com',
    'www.bbc.co.uk',          # example trusted hosts
}

# Helper: check if an IP is private/internal
def _is_internal_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a valid IP address; treat as non‑internal
        return False

# Resolve hostname to all IPv4/IPv6 addresses and check for internal ones
def _has_internal_ip(hostname: str) -> bool:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # Cannot resolve hostname; treat as untrusted
        return True
    for _, _, _, _, sockaddr in infos:
        ip_str = sockaddr[0]
        if _is_internal_ip(ip_str):
            return True
    return False

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL supplied by the user.

    Returns
    -------
    str
        The validated, trusted RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, does not belong to a trusted provider,
        or resolves to an internal network address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    # Basic URL validation
    parsed = urlparse(rss_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Normalize the hostname for comparison
    hostname_lower = hostname.lower()

    # Check against trusted list
    if hostname_lower not in TRUSTED_HOSTNAMES:
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Ensure the hostname does not resolve to an internal IP
    if _has_internal_ip(hostname_lower):
        raise ValueError(f"Hostname '{hostname}' resolves to an internal IP address")

    # Reconstruct the URL safely
    cleaned_url = parsed.geturl()
    # Optionally, unquote percent-encoded parts for consistency
    cleaned_url = unquote(cleaned_url)

    return cleaned_url