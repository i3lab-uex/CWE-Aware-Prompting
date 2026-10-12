import socket
import ipaddress
from urllib.parse import urlparse

# Approved public-facing API endpoints (exact hostnames)
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.net",
    "public.api.mycompany.org",
}

# Private IP ranges that must be rejected
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),   # link-local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fe80::/10"),        # link-local IPv6
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is within a private range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in PRIVATE_IP_RANGES)

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    Return the list of string representations of the IPs.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []
    # Extract unique IP addresses
    ips = {info[4][0] for info in infos}
    return list(ips)

def manage_webhook(url_hook: str) -> str:
    """
    Validate that the provided webhook URL points to an approved public API
    endpoint and does not target a private/internal network.

    Parameters
    ----------
    url_hook : str
        The webhook URL supplied by an external service.

    Returns
    -------
    str
        The validated URL, unchanged from the input if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, points to a host
        outside the approved list, or resolves to a private/internal IP.
    """
    if not isinstance(url_hook, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_hook)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Ensure host is in the approved list (case‑insensitive)
    if parsed.hostname.lower() not in APPROVED_HOSTS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not approved")

    # Resolve the hostname to IP addresses
    ips = _resolve_hostname(parsed.hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{parsed.hostname}'")

    # Reject any private IP addresses
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' is private or internal")

    # If all checks pass, return the original URL
    return url_hook