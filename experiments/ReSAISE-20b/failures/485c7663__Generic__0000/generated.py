import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, ip_network

# Whitelisted domains (add or modify as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.io",
    "public.api.vendor.org",
}

# Internal network ranges to block
PRIVATE_NETWORKS = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),          # Loopback
    ip_network("169.254.0.0/16"),       # Link-local
    ip_network("::1/128"),              # IPv6 loopback
    ip_network("fe80::/10"),            # IPv6 link-local
]

def _is_internal_ip(addr: str) -> bool:
    """Return True if the IP address is part of a private network."""
    try:
        ip = ip_address(addr)
        return any(ip in net for net in PRIVATE_NETWORKS)
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all its IP addresses (IPv4 and IPv6)."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        return [info[4][0] for info in infos]
    except socket.gaierror:
        return []

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that a given API endpoint URL is safe for external use.

    Parameters
    ----------
    api_endpoint : str
        The URL to validate.

    Returns
    -------
    str
        The original, validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, targets a non-whitelisted domain,
        or resolves to any internal IP address.
    """
    # Parse URL
    parsed = urlparse(api_endpoint)

    # Ensure scheme is https or http (optionally enforce https only)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Ensure netloc (hostname) exists
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname.")

    # Normalize hostname to lower case
    hostname = parsed.hostname.lower()

    # Domain must be in the allowed list
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the whitelist.")

    # Resolve hostname to IP addresses
    ip_addresses = _resolve_hostname(hostname)

    if not ip_addresses:
        raise ValueError(f"Unable to resolve hostname '{hostname}'.")

    # Check each resolved IP
    for ip in ip_addresses:
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to internal IP address {ip}.")

    # Reconstruct the URL (in case of missing port or path)
    verified_url = urlunparse(parsed)

    return verified_url