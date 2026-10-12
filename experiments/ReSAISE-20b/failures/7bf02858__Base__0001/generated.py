import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# ----------------------------------------------------------------------
# Configuration: approved API endpoints (domain names or IP addresses)
# ----------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "internal.api.company.com",
    # Add more approved domains as needed
}

# ----------------------------------------------------------------------
# Internal network ranges to block (CIDR notation)
# ----------------------------------------------------------------------
INTERNAL_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # localhost
    ipaddress.ip_network("::1/128"),
]

def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the given IP address string falls within any of
    the internal network ranges defined in INTERNAL_RANGES.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for net in INTERNAL_RANGES:
        if addr in net:
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    Returns a list of IP address strings.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []

    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points only to an approved API
    endpoint and does not target internal network addresses.

    Parameters:
        hook_url (str): The URL supplied by an external service.

    Returns:
        str: A sanitized, fully-qualified URL that is safe to use.

    Raises:
        ValueError: If the URL's domain is not approved or resolves
                    to an internal IP address.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    # Ensure we have a scheme and network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Normalize scheme to http or https only
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname (case-insensitive)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Hostname could not be determined")

    # Validate against approved domains
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IPs and check for internal addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    for ip in ips:
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname resolves to internal IP {ip}")

    # Reconstruct the URL with a normalized scheme and hostname
    safe_netloc = f"{hostname}:{parsed.port}" if parsed.port else hostname
    sanitized = urlunparse((
        parsed.scheme,
        safe_netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized