import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    'api.example.com',
    'internal.api.example.com',
}

# IPv4 private ranges (CIDR)
PRIVATE_RANGES = [
    ('10.0.0.0', '10.255.255.255'),
    ('172.16.0.0', '172.31.255.255'),
    ('192.168.0.0', '192.168.255.255'),
    # Loopback
    ('127.0.0.0', '127.255.255.255'),
]

# IPv6 private ranges
PRIVATE_RANGES += [
    ('fc00::', 'fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'),
    ('fe80::', 'febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff'),
    ('::1', '::1'),  # loopback
]

def _ip_to_int(ip: str) -> int:
    """Convert an IPv4/IPv6 address string to a 128‑bit integer."""
    if ':' in ip:   # IPv6
        return int(socket.inet_pton(socket.AF_INET6, ip).hex(), 16)
    else:           # IPv4
        return int(socket.inet_aton(ip).hex(), 16)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    ip_int = _ip_to_int(ip)
    for start, end in PRIVATE_RANGES:
        if _is_ip_in_range(ip_int, start, end):
            return True
    return False

def _is_ip_in_range(ip_int: int, start: str, end: str) -> bool:
    """Check if ip_int is between start and end inclusive."""
    return _ip_to_int(start) <= ip_int <= _ip_to_int(end)

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A sanitized and validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        references a disallowed domain, or resolves to a private IP address.
    """
    # Basic syntax check
    parsed = urlparse(hook_url)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Normalise the domain (case‑insensitive)
    hostname_lower = hostname.lower()
    if hostname_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {hostname}") from exc

    # Ensure all resolved IPs are public
    for entry in addrinfo:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or loopback")

    # Re‑assemble the URL to avoid any malicious path manipulation
    safe_url = urlunparse((
        parsed.scheme,
        f"{hostname}:{parsed.port}" if parsed.port else hostname,
        parsed.path or '',
        '',  # params
        '',  # query
        ''   # fragment
    ))

    return safe_url