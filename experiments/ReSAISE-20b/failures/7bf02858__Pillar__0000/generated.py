import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# Approved domains or domain patterns (regex)
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^service\.trusted\.org$",
    r"^internal\.company\.com$",
]

# Private IP ranges to block
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
]

def _is_approved_domain(domain: str) -> bool:
    """Check if the domain matches one of the approved patterns."""
    for pattern in APPROVED_DOMAINS:
        if re.match(pattern, domain, re.IGNORECASE):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def _resolve_and_check(domain: str) -> None:
    """
    Resolve the domain to its IP addresses and ensure none are private.
    Raises ValueError if a private or invalid address is found.
    """
    try:
        # Resolve all addresses for the domain
        addr_info = socket.getaddrinfo(domain, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve domain '{domain}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Domain '{domain}' resolves to a private IP ({ip})")

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points only to approved API endpoints.

    Parameters
    ----------
    hook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it resolves to an internal network location.
    """
    # Basic parsing
    parsed: ParseResult = urlparse(hook_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{hook_url}'")

    # Enforce HTTPS to avoid downgrade attacks
    if parsed.scheme.lower() != "https":
        raise ValueError(f"URL scheme must be HTTPS: '{parsed.scheme}'")

    domain = parsed.hostname
    if not domain:
        raise ValueError(f"URL missing hostname: '{hook_url}'")

    # Check against approved domain patterns
    if not _is_approved_domain(domain):
        raise ValueError(f"Domain '{domain}' is not approved")

    # Resolve domain and ensure no private IPs
    _resolve_and_check(domain)

    # Reconstruct the URL to normalize it (e.g., lower-case scheme and host)
    safe_url = parsed._replace(
        scheme="https",
        netloc=f"{domain}:{parsed.port}" if parsed.port else domain
    ).geturl()

    return safe_url