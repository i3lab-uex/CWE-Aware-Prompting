import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of approved domain patterns (regex).  Adjust as needed.
APPROVED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\.trustedprovider\.org$",
]

# IP ranges that are considered internal/private
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("::1/128"),          # loopback
    ipaddress.IPv4Network("127.0.0.0/8"),       # loopback
    ipaddress.IPv6Network("fc00::/7"),          # unique local address (ULA)
    ipaddress.IPv6Network("fe80::/10"),         # link local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls within a private/internal range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # If not a valid IP address, consider it unsafe
        return True
    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def _is_approved_domain(domain: str) -> bool:
    """Check whether the domain matches one of the approved patterns."""
    for pattern in APPROVED_DOMAIN_PATTERNS:
        if re.match(pattern, domain, flags=re.IGNORECASE):
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate an external API URL and ensure it points to a public, approved endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL to validate.

    Returns
    -------
    str
        The validated and normalized URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL uses an unsafe scheme, points to a private IP or domain,
        or does not match any approved domain pattern.
    """
    # Basic parsing
    parsed = urlparse(api_endpoint)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname.")

    # Resolve the hostname to IP addresses
    try:
        # Use getaddrinfo for IPv4 and IPv6 support
        addr_info = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{parsed.hostname}': {exc}") from exc

    # Check each resolved IP address
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{parsed.hostname}' resolves to a private IP ({ip}).")

    # Validate domain against approved list
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the approved domain list.")

    # Reconstruct a normalized URL (strip default port, etc.)
    netloc = parsed.hostname
    if parsed.port and parsed.port != 443:
        netloc += f":{parsed.port}"
    normalized = parsed._replace(netloc=netloc).geturl()
    return normalized