import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of fully qualified domain names that are considered trusted
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "trusted.api.net",
}

# Regular expression to detect any IPv4 or IPv6 address in a hostname
IP_ADDRESS_REGEX = re.compile(
    r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"  # IPv4
    r"|^"
    r"\[?[0-9a-fA-F:]+\]?$"            # IPv6
)

# Private/reserved IP ranges that must be blocked
PRIVATE_IP_RANGES = [
    ip_address("0.0.0.0") / 8,
    ip_address("10.0.0.0") / 8,
    ip_address("127.0.0.0") / 8,
    ip_address("169.254.0.0") / 16,
    ip_address("172.16.0.0") / 12,
    ip_address("192.168.0.0") / 16,
    ip_address("224.0.0.0") / 4,   # Multicast
    ip_address("240.0.0.0") / 4,   # Reserved
    ip_address("::1") / 128,
    ip_address("fc00::") / 7,      # Unique local
    ip_address("fe80::") / 10,     # Link-local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or reserved range."""
    try:
        ip_obj = ip_address(ip)
    except ValueError:
        return False
    for network in PRIVATE_IP_RANGES:
        if ip_obj in network:
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to its IPv4/IPv6 addresses."""
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        return list({ai[4][0] for ai in addr_info})
    except socket.gaierror:
        return []

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Basic URL parsing
    parsed = urlparse(api_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and host")

    # Normalize the URL (remove fragment, etc.)
    normalized = urlunparse((parsed.scheme, parsed.netloc,
                             parsed.path or "", parsed.params or "",
                             parsed.query or "", ""))

    # Extract hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that directly specify an IP address
    if IP_ADDRESS_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError("URL resolves to a private IP address")
        # If it's a public IP, ensure it's allowed
        if not any(_is_private_ip(ip) for ip in _resolve_hostname(host)):
            # public IP allowed only if domain is trusted
            pass

    # Check against the list of trusted domains (exact match)
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # Resolve hostname and ensure none of the IPs are private
    resolved_ips = _resolve_hostname(host)
    if not resolved_ips:
        raise ValueError(f"Could not resolve hostname '{host}'")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP '{ip}'")

    return normalized