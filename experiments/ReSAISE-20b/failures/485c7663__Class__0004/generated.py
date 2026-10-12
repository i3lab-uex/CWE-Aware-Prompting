import re
import socket
from urllib.parse import urlparse, ParseResult
import ipaddress

# A set of domains that are explicitly allowed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    # Add more approved domains here.
}

# Regular expression to quickly reject obvious non‑HTTPS URLs
HTTPS_RE = re.compile(r"^https://", re.IGNORECASE)

# Private / reserved IP blocks that should never be reachable
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv6Network("::1/128"),
    ipaddress.IPv6Network("fc00::/7"),
    ipaddress.IPv6Network("fe80::/10"),
]

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address belongs to a private or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for network in PRIVATE_IP_RANGES:
        if addr in network:
            return True
    return False

def _resolve_host_to_ips(hostname: str) -> set[str]:
    """
    Resolve a hostname to all its IPv4/IPv6 addresses.
    Returns an empty set if resolution fails.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
        return {socket.inet_ntoa(info[4][0]) if info[0] == socket.AF_INET else
                socket.inet_ntop(socket.AF_INET6, info[4][0]) for info in infos}
    except socket.gaierror:
        return set()

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the provided URL points to an approved external API endpoint.
    
    Parameters
    ----------
    api_endpoint : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL uses a disallowed scheme, resolves to an internal IP,
        or its hostname is not in the list of approved domains.
    """
    # Quick scheme check
    if not HTTPS_RE.match(api_endpoint):
        raise ValueError("Only HTTPS URLs are allowed")

    parsed: ParseResult = urlparse(api_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject IP addresses in the URL directly
    try:
        ipaddress.ip_address(hostname)
        # If parsing succeeded, the hostname is an IP literal
        if _is_private_ip(hostname):
            raise ValueError("URL resolves to a private IP address")
    except ValueError:
        # Not an IP literal; resolve the hostname
        ips = _resolve_host_to_ips(hostname)
        if not ips:
            raise ValueError("Unable to resolve hostname")
        for ip in ips:
            if _is_private_ip(ip):
                raise ValueError(f"Hostname resolves to private IP {ip}")

    # Ensure the hostname is in the approved list
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not approved")

    return api_endpoint