import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# A set of domains that are considered trusted.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.net",
    "data.partner.org",
}

# Regular expression for common private IP ranges (IPv4 only)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or reserved."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def _resolve_host(host: str) -> list[str]:
    """Resolve the hostname to a list of IP addresses."""
    try:
        return socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def check_api_link(api_link: str) -> str:
    """
    Validate that an API link points to a trusted external domain
    and does not resolve to private or internal IP addresses.

    Parameters:
        api_link (str): The URL to validate.

    Returns:
        str: The validated, normalized URL.

    Raises:
        ValueError: If the URL is not trusted or points to an internal IP.
    """
    # Parse and normalise
    parsed = urlparse(api_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Ensure the hostname is in the trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not a trusted domain")

    # Resolve the host to IP addresses
    addrinfo = _resolve_host(host)
    if not addrinfo:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Check each resolved IP address
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {host} resolves to a private IP ({ip})")

    # Reconstruct the URL (normalise case, remove fragments)
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        "",  # fragment removed
    ))
    return normalized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = check_api_link("https://api.example.com/v1/data")
        print(f"Validated URL: {safe_url}")
    except ValueError as e:
        print(f"URL validation failed: {e}")