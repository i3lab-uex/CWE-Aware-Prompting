import ipaddress
import socket
from urllib.parse import urlparse

# List of trusted RSS providers (you can extend this list)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that the provided RSS feed URL originates from a trusted provider
    and does not point to an internal network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The validated URL if it is trusted and external.

    Raises:
        ValueError: If the URL is malformed, points to an untrusted domain,
                    or resolves to an internal IP address.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Ensure the domain is in the trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve the hostname to IP(s) and check for internal addresses
    try:
        ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in ips:
        ip = sockaddr[0]
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is internal")

    return url