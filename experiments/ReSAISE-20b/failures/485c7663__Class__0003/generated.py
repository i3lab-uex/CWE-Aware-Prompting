import socket
import ipaddress
from urllib.parse import urlparse

# List of CIDR blocks that represent private/internal networks (CWE‑441 risk).
_PRIVATE_CIDRS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),     # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),        # IPv6 loopback
    ipaddress.ip_network("fc00::/7")       # unique local IPv6 addresses
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls into any private CIDR block."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for cidr in _PRIVATE_CIDRS:
        if addr in cidr:
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the given URL points to a secure, external API endpoint.

    Raises:
        ValueError: If the URL is not HTTPS or resolves to an internal IP address.
    Returns:
        str: The original, verified URL.
    """
    parsed = urlparse(api_endpoint)

    # Must use HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for API endpoints")

    # Resolve host to IP addresses
    try:
        host_ips = socket.gethostbyname_ex(parsed.hostname)[2]
    except Exception as exc:
        raise ValueError(f"Unable to resolve hostname {parsed.hostname!r}") from exc

    # Check that none of the resolved IPs are private/internal
    for ip in host_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {parsed.hostname!r} resolves to internal IP {ip}")

    # Optional: check that the URL is not pointing to a known proxy or gateway
    # (e.g., "http://localhost:8000") – we already reject non-HTTPS and internal IPs.

    return api_endpoint