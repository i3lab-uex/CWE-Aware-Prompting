import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of trusted domain names (case‑insensitive)
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net",
}

# Private IP ranges (RFC 1918 + others)
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),        # Loopback
    ipaddress.ip_network("169.254.0.0/16"),     # Link local
    ipaddress.ip_network("::1/128"),           # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),         # IPv6 link local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False
    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all its IP addresses."""
    try:
        # getaddrinfo returns tuples; the 4th element is the IP address
        return [res[4][0] for res in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or resolves to a private IP.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Normalize hostname for case‑insensitive comparison
    host = parsed.hostname.lower()
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve the hostname to IP addresses
    ips = _resolve_hostname(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Ensure none of the resolved IPs are private
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {host} resolves to private IP: {ip}")

    # Reconstruct the URL to ensure canonical form
    validated_url = urlunparse(parsed._replace(netloc=host + (f":{parsed.port}" if parsed.port else "")))
    return validated_url