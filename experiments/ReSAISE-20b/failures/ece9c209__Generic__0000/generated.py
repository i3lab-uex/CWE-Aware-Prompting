import re
import socket
from urllib.parse import urlparse

# Allowed top‑level domains or specific hostnames for the trusted API.
ALLOWED_DOMAINS = {
    "api.example.com",
    "trusted.api.service",
}

# Regular expression for IP addresses (IPv4 & IPv6)
IPV4_RE = re.compile(
    r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
)
IPV6_RE = re.compile(
    r"^\[?[0-9a-fA-F:]+\]?$"
)

# Private / non‑public IP ranges that should be rejected
PRIVATE_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),   # loopback
    ("169.254.0.0", "169.254.255.255"), # link‑local
    ("::1", "::1"),                     # IPv6 loopback
]

def ip_to_int(ip: str) -> int:
    """Convert an IPv4 address string to a 32‑bit integer."""
    parts = [int(p) for p in ip.split(".")]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls in a private or non‑public range."""
    try:
        # IPv4
        if IPV4_RE.match(ip):
            ip_int = ip_to_int(ip)
            for start, end in PRIVATE_RANGES[:5]:
                if ip_to_int(start) <= ip_int <= ip_to_int(end):
                    return True
            return False
        # IPv6 is rejected outright for simplicity (could be expanded)
        if IPV6_RE.match(ip):
            return True
    except Exception:
        pass
    return False

def resolve_host(host: str) -> list[str]:
    """Return a list of IP addresses for the given host."""
    try:
        return socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL does not resolve to an allowed domain or attempts to reach
        a private/internal network address.
    """
    if not api_url:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(api_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against the allowed domain list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of allowed domains")

    # Resolve host to IP(s) and ensure none are private
    addresses = resolve_host(host)
    if not addresses:
        raise ValueError(f"Could not resolve host '{host}'")

    for addr in addresses:
        ip = addr[4][0]
        if is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or internal")

    # All checks passed
    return api_url