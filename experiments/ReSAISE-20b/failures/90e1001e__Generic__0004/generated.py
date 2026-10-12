import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved domain patterns (regex or plain strings)
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^data\.trustedservice\.org$",
    r"^services\.mycompany\.net$",
]

# Regular expression to detect private IP ranges
PRIVATE_IP_RANGES = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^::1$"),  # IPv6 loopback
]

def is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls into a private or reserved range."""
    # IPv6 check
    try:
        import ipaddress
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except Exception:
        pass

    for pattern in PRIVATE_IP_RANGES:
        if pattern.match(ip):
            return True
    return False

def validate_service_url(service_url: str) -> str:
    """
    Validate that the provided URL points to an approved external API.
    
    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        Normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain, uses an insecure scheme,
        or resolves to a private/internal IP address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)

    # Enforce https scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname.")

    # Check against approved domains
    if not any(re.match(pattern, host) for pattern in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved.")

    # Resolve hostname to IP(s) and ensure none are private
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or internal.")

    # Reconstruct the URL (ensure scheme lower-case)
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or '',
        parsed.params or '',
        parsed.query or '',
        parsed.fragment or ''
    ))

    return normalized