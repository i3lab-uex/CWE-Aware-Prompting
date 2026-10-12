import urllib.parse
import socket
import ipaddress
from typing import Set

# List of approved API domains (lower‑case for case‑insensitive comparison)
APPROVED_DOMAINS: Set[str] = {
    "api.example.com",
    "internal.api.example.com",
}

# Internal network ranges that must be rejected
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),            # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),           # IPv6 link‑local
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def _resolve_hostname(hostname: str) -> Set[str]:
    """
    Resolve the hostname to all IP addresses.
    Return a set of stringified IPs. If resolution fails, return an empty set.
    """
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
        return set(ips)
    except (socket.gaierror, UnicodeError):
        return set()

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL against approved API endpoints.

    Args:
        webhook_link: The raw URL supplied by an external service.

    Returns:
        A validated, normalised URL that points to an approved endpoint.

    Raises:
        ValueError: If the URL's domain is not in APPROVED_DOMAINS or
                    points to an internal network location.
    """
    if not webhook_link:
        raise ValueError("Webhook link must be a non‑empty string")

    # Parse the URL and normalise components
    parsed = urllib.parse.urlparse(webhook_link)
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal network addresses
    if _is_private_ip(hostname):
        raise ValueError(f"Hostname {hostname} resolves to a private IP")

    # Resolve hostname to check for private IPs
    ips = _resolve_hostname(hostname)
    if not ips:
        # If we cannot resolve, be conservative and reject
        raise ValueError(f"Hostname {hostname} could not be resolved")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")

    # Validate against approved domains (case‑insensitive)
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname {hostname} is not an approved API endpoint")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urllib.parse.urlunparse((
        scheme,
        parsed.netloc,
        urllib.parse.quote(parsed.path or "/"),
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))

    return safe_url