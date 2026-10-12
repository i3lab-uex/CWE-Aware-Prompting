import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (example entries)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public-api.service.org",
    "api.partner.net",
}

# Disallowed IP ranges (private, loopback, link-local, etc.)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),         # Unique local address (ULA)
]

def _is_ip_private(ip_str: str) -> bool:
    """Return True if the IP address is in a private range."""
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        # Not a valid IP address
        return False
    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def _is_domain_whitelisted(domain: str) -> bool:
    """Check if the domain is in the approved whitelist."""
    return domain.lower() in WHITELISTED_DOMAINS

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API endpoints
    and ensure it does not resolve to a private or internal IP address.

    Args:
        webhook_endpoint (str): The external webhook URL to validate.

    Returns:
        str: The validated and sanitized URL ready for internal API calls.

    Raises:
        ValueError: If the URL's domain is not whitelisted or resolves to a private IP.
    """
    if not webhook_endpoint:
        raise ValueError("Webhook endpoint must be a non-empty string")

    parsed = urlparse(webhook_endpoint)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check whitelist
    if not _is_domain_whitelisted(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Resolve hostname to IP addresses and check for private ranges
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {e}") from e

    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if _is_ip_private(ip_str):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip_str}")

    # Reconstruct a safe URL (ensuring no userinfo or fragment)
    safe_parts = (
        parsed.scheme,
        parsed.netloc.split("@")[-1],  # remove userinfo if present
        parsed.path,
        "",  # params
        "",  # query (could preserve if needed)
        ""   # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url