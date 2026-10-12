import ipaddress
from urllib.parse import urlparse

# List of trusted RSS feed domains (add more as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.reddit.com",
    "medium.com/feed",
}

# Private IP network ranges that should never be accessed
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address belongs to a private network.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Invalid IP address string
        return False
    for net in _PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from an approved external provider
    and does not point to any internal or private network address.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Basic parsing
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url}")

    # Ensure the scheme is HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}': {url}")

    # Check domain against whitelist
    host = parsed.hostname or ""
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain '{host}' in URL: {url}")

    # Optional: Resolve host to IP and ensure it is not private
    # (Note: This performs a DNS lookup; skip if you want purely static checks)
    try:
        import socket
        ip = socket.gethostbyname(host)
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP {ip}: {url}")
    except Exception:
        # If DNS resolution fails, treat as invalid
        raise ValueError(f"Unable to resolve host '{host}' for URL: {url}")

    return url