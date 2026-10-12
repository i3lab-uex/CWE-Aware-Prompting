import re
import socket
from urllib.parse import urlparse

# Common private IP ranges in CIDR notation
_PRIVATE_CIDRS = [
    re.compile(r"^10\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^127\."),
    re.compile(r"^169\.254\."),  # Link-local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    for pattern in _PRIVATE_CIDRS:
        if pattern.match(ip):
            return True
    return False

def _resolve_ip(hostname: str) -> str:
    """Resolve hostname to an IPv4 address (first match)."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname: {hostname}") from exc

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that the provided URL points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_url : str
        The URL to be validated.

    Returns
    -------
    str
        The verified URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, resolves to a private IP,
        or cannot be resolved.
    """
    parsed = urlparse(endpoint_url)

    # 1. Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # 2. Must contain a hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Resolve the hostname to an IP address
    ip_address = _resolve_ip(parsed.hostname)

    # 4. Reject private/internal IP addresses
    if _is_private_ip(ip_address):
        raise ValueError(f"Endpoint resolves to a private IP: {ip_address}")

    # 5. Return the original URL (it is considered safe)
    return endpoint_url