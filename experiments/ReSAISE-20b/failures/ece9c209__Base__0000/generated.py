import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted API domains (regex patterns or exact strings)
ALLOWED_DOMAINS = [
    r"^api\.trustedservice\.com$",
    r"^data\.secure\.org$",
    # add more patterns or exact hostnames as needed
]

# Compile regex for faster matching
ALLOWED_REGEX = [re.compile(pattern) for pattern in ALLOWED_DOMAINS]

# IP ranges that are considered unsafe (private, loopback, link-local, etc.)
UNSAFE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),           # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),         # IPv6 link-local
    ipaddress.ip_network("fc00::/7"),          # IPv6 unique local
]


def _is_ip_safe(ip: str) -> bool:
    """Return True if the IP address is not in any unsafe range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # Invalid IP address
        return False

    for network in UNSAFE_IP_RANGES:
        if ip_obj in network:
            return False
    return True


def _is_domain_allowed(hostname: str) -> bool:
    """Check if the hostname matches one of the allowed domain patterns."""
    for regex in ALLOWED_REGEX:
        if regex.match(hostname.lower()):
            return True
    return False


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that a URL points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, guaranteed to point to a trusted API.

    Raises
    ------
    ValueError
        If the URL is not part of the allowed API domains or attempts to reach internal addresses.
    """
    # Parse URL
    parsed = urlparse(api_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host: {exc}") from exc

    # Ensure at least one IP is safe
    safe_ip_found = False
    for entry in addr_info:
        ip_addr = entry[4][0]
        if _is_ip_safe(ip_addr):
            safe_ip_found = True
            break

    if not safe_ip_found:
        raise ValueError("Resolved IP address is in an unsafe/private range")

    # Check domain against allowed patterns
    if not _is_domain_allowed(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the list of allowed domains")

    # Rebuild URL to avoid any encoded tricks (e.g., percent-encoded hostname)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized