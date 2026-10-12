import re
from urllib.parse import urlparse, unquote
import socket
import ipaddress

# List of trusted providers (example domains).  Add or remove as needed.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "feeds.reuters.com",
    "rss.cnn.com",
}

# Regular expression to detect private IP addresses (IPv4)
_PRIVATE_IPV4_RE = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

# Regular expression to detect private IP addresses (IPv6)
_PRIVATE_IPV6_RE = re.compile(r"^(fd|fe80::)")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private or link-local."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        return False

def _resolve_host_to_ip(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4 and IPv6 addresses."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def check_rss_source(source_url: str) -> str:
    """
    Validate that the provided RSS feed URL originates from a trusted provider
    and does not point to an internal or private network address.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated URL unchanged if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    # Parse the URL and ensure it has a scheme
    parsed = urlparse(source_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must have http or https scheme")

    # Normalize the hostname (case-insensitive)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious private IPs in the host string
    if _PRIVATE_IPV4_RE.match(hostname) or _PRIVATE_IPV6_RE.match(hostname):
        raise ValueError("URL resolves to a private IP address")

    # Check against the trusted domain list
    if hostname.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Resolve the hostname to IP addresses and ensure none are private
    addrinfo = _resolve_host_to_ip(hostname)
    if not addrinfo:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or internal")

    # If all checks pass, return the original URL (unmodified)
    return source_url