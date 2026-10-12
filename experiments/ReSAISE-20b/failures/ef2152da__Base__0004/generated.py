import ipaddress
import socket
from urllib.parse import urlparse

# Whitelisted public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "public.api.service.net",
}

# IP address networks that are considered private/internal
PRIVATE_NETWORKS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),   # Unique local addresses
    ipaddress.IPv6Network("fe80::/10"),  # Link-local addresses
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or internal range."""
    addr = ipaddress.ip_address(ip)
    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API
    endpoints and ensure it does not resolve to a private/internal IP.

    Args:
        callback_url: External webhook URL supplied by an upstream component.

    Returns:
        The original URL if it is safe to use for internal API calls.

    Raises:
        ValueError: If the domain is not whitelisted or resolves to a private IP.
    """
    if not callback_url:
        raise ValueError("Callback URL must be provided")

    parsed = urlparse(callback_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Normalise the domain (remove port if present)
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # Verify none of the resolved IPs are private/internal
    for entry in addrinfo:
        sockaddr = entry[4]
        ip_addr = sockaddr[0]  # IPv4 or IPv6 string
        if _is_private_ip(ip_addr):
            raise ValueError(
                f"Resolved IP '{ip_addr}' for host '{host}' is private or internal"
            )

    # If all checks pass, return the original URL
    return callback_url