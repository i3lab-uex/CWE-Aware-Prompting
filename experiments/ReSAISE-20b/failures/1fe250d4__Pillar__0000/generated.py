import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Approved domains (example).  Add any external domain you trust here.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

# Regex for valid hostnames (simplified)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private, loopback or link‑local range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to its IPv4/IPv6 addresses."""
    try:
        infos = socket.getaddrinfo(host, None)
        return [sock[4][0] for sock in infos]
    except socket.gaierror:
        return []

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to an approved external API endpoint.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain or resolves to a private IP.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(endpoint_url)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Validate hostname format
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"Invalid hostname: {host}")

    # Ensure host is in the allowed list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # Resolve host to IPs and check for private addresses
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # Reconstruct the URL to ensure consistent formatting
    cleaned_url = urlunparse(parsed._replace(netloc=host))
    return cleaned_url