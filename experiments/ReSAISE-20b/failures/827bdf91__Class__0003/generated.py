import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of trusted providers – expand as needed
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    # Add more trusted domains here
}

# Regular expression to detect private or loopback IP addresses in the URL
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is a private or loopback address."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to its IP addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL supplied by the caller.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, or if it attempts to access
        an internal network or private IP address.
    """
    # Basic URL parsing and scheme validation
    parsed = urlparse(rss_url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    netloc = parsed.hostname
    if not netloc:
        raise ValueError("URL must contain a hostname")

    # Check against the trusted domain list
    if netloc.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not trusted")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_host(netloc)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {netloc}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to a private IP: {ip}")

    # Reconstruct the URL to ensure no path traversal or query tricks
    sanitized = urlunparse((
        parsed.scheme,
        netloc.lower(),
        parsed.path if parsed.path else "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized