import socket
import ipaddress
from urllib.parse import urlparse

# List of approved domains (wildcards not supported in this simple example)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    "services.google.com",
}

# List of IP networks that are considered internal/private
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address belongs to a private or link-local range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False
    return any(ip_obj in net for net in PRIVATE_IP_RANGES)

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all its IPv4 and IPv6 addresses."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def validate_service_url(service_url: str) -> str:
    """
    Validate that the given URL points to an approved external API and does not target
    internal network addresses.

    Parameters
    ----------
    service_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it resolves to a private IP.
    """
    parsed = urlparse(service_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Ensure the hostname is in the approved list
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the list of approved domains")

    # Resolve hostname to IP addresses
    addrinfo = _resolve_hostname(hostname)
    if not addrinfo:
        raise ValueError(f"Unable to resolve hostname '{hostname}'")

    # Verify that none of the resolved IPs are private
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address ({ip})")

    return service_url