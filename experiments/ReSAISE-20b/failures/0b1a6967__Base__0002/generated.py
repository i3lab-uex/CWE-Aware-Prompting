import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Allowed domains (case‑insensitive). Add more as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

# Regex for allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # Treat non‑IP values as invalid
    return addr.is_private or addr.is_loopback or addr.is_reserved

def _resolve_host(host: str) -> set[str]:
    """Return a set of IP addresses resolved for the host."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return set()
    ips = {info[4][0] for info in infos}
    return ips

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the given URL points to an approved external API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, targets a private IP,
        or resolves to an unapproved domain.
    """
    # Basic parsing
    parsed = urlparse(endpoint_address)

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Normalize host (remove port)
    host = parsed.hostname
    if not host:
        raise ValueError("Could not determine hostname")

    # Check against allowed domains
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve host to IPs and reject private addresses
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve host: {host}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Host resolves to private IP: {ip}")

    # Rebuild the URL to ensure canonical form
    verified = urlunparse(parsed._replace())
    return verified