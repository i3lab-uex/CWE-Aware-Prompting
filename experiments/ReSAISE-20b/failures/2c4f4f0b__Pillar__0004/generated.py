import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of trusted RSS providers (hostnames or subdomains)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.bbc.co.uk",
    "feeds.npr.org",
    "wikipedia.org",          # e.g., feeds.wikipedia.org
}

# Regular expression to detect private IP address patterns (IPv4 only)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private address."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; assume not private
        return False

def _resolve_host_to_ip(hostname: str) -> str:
    """Resolve a hostname to its canonical IPv4 address."""
    try:
        # Use getaddrinfo to avoid DNS rebinding issues
        addr_info = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
        # Return the first IPv4 address found
        return addr_info[0][4][0]
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL originates from a trusted provider
    and does not point to an internal/private network address.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, from an untrusted provider,
        or resolves to a private/internal IP address.
    """
    # Basic URL parsing
    parsed = urlparse(source_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {source_url}")

    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError(f"Could not extract hostname from URL: {source_url}")

    # Check against trusted provider list
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Resolve hostname to IP and ensure it is not private
    ip = _resolve_host_to_ip(hostname)

    # First, use regex for quick private IP check
    if PRIVATE_IP_REGEX.match(ip):
        raise ValueError(f"URL resolves to a private IP address: {ip}")

    # Additional safety check using ipaddress module
    if _is_private_ip(ip):
        raise ValueError(f"URL resolves to a private IP address: {ip}")

    # All checks passed
    return source_url