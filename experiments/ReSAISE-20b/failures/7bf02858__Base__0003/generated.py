import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved public API endpoints (hostnames or subdomains)
APPROVED_HOSTS = {
    "api.example.com",
    "service.foo.org",
    # Add more approved hosts here
}

# Regular expression to detect IPv4/IPv6 addresses in URLs
IP_PATTERN = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$|^\[?[A-F0-9:]+\]?$',
                         re.IGNORECASE)


def _is_private_ip(ip_address: str) -> bool:
    """
    Determine if the given IP address is within private or loopback ranges.
    Supports both IPv4 and IPv6 addresses.
    """
    try:
        ip_obj = socket.inet_pton(socket.AF_INET, ip_address)
    except OSError:
        # Not an IPv4 address; try IPv6
        try:
            ip_obj = socket.inet_pton(socket.AF_INET6, ip_address)
        except OSError:
            return False  # not a valid IP address

    # Convert to integer for comparison
    if ':' in ip_address:  # IPv6
        return (
            ip_obj.startswith(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            or ip_obj.startswith(b'\xFF\xFF')  # link-local
        )
    else:  # IPv4
        parts = list(map(int, ip_address.split('.')))
        if parts[0] == 10:
            return True
        if parts[0] == 172 and 16 <= parts[1] <= 31:
            return True
        if parts[0] == 192 and parts[1] == 168:
            return True
        if ip_address == "127.0.0.1":
            return True
    return False


def _is_internal_host(host: str) -> bool:
    """
    Resolve the host to an IP and check if it is private or loopback.
    """
    try:
        # Resolve all addresses for the host
        addrs = socket.getaddrinfo(host, None)
    except socket.gaierror:
        # Host could not be resolved; treat as invalid
        return True

    for family, _, _, _, sockaddr in addrs:
        if family == socket.AF_INET:  # IPv4
            ip = sockaddr[0]
        elif family == socket.AF_INET6:  # IPv6
            ip = sockaddr[0]
        else:
            continue

        if _is_private_ip(ip):
            return True
    return False


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL before it is used to call an internal API.

    Parameters
    ----------
    hook_url : str
        The URL provided by the external service.

    Returns
    -------
    str
        The original URL if it is safe and approved.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or points to an internal network.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that are IP addresses or internal hosts
    if IP_PATTERN.match(host) or _is_internal_host(host):
        raise ValueError(f"URL host '{host}' is not allowed (internal or IP address)")

    # Ensure the host matches an approved endpoint
    if host not in APPROVED_HOSTS:
        raise ValueError(f"URL host '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure no hidden payload (e.g., port manipulation)
    safe_url = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or '',
        parsed.params or '',
        parsed.query or '',
        parsed.fragment or ''
    ))

    return safe_url