import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, ip_network

# ----------------------------------------------------------------------
# Configuration: whitelist of approved public API domains
# ----------------------------------------------------------------------
WHITELISTED_DOMAINS = {
    "api.example.com",
    "service.provider.net",
    "public.api.org"
}

# Internal/private network ranges that must be blocked
PRIVATE_NETWORKS = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),          # Loopback
    ip_network("169.254.0.0/16"),       # Link-local
]

# ----------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is within any of
    PRIVATE_NETWORKS. Raises ValueError for invalid addresses.
    """
    try:
        addr = ip_address(ip)
    except ValueError as exc:
        raise ValueError(f"Invalid IP address: {ip}") from exc

    return any(addr in net for net in PRIVATE_NETWORKS)

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IPv4 and IPv6 addresses.
    Return a list of string IPs. Raise ValueError if resolution fails.
    """
    try:
        # getaddrinfo returns tuples; we only need the address part
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}'") from exc

    return [info[4][0] for info in infos]

# ----------------------------------------------------------------------
def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API
    endpoints and ensure it does not target private or internal network
    addresses. Return the sanitized URL for internal use.

    Parameters:
        webhook_endpoint (str): The external webhook URL to validate.

    Returns:
        str: A validated, fully qualified URL safe for internal API calls.

    Raises:
        ValueError: If the domain is not whitelisted or resolves to a
                    private/internal IP address.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("webhook_endpoint must be a string")

    # Parse the URL and normalise
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed")

    # Validate domain against whitelist
    hostname = parsed.hostname.lower()
    if hostname not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Resolve hostname to IP addresses and check for private ranges
    resolved_ips = _resolve_hostname(hostname)
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{hostname}' is private/internal")

    # Reconstruct the URL to ensure no malicious fragments or queries
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        '',          # params
        '',          # query - strip all queries to avoid leaking data
        ''           # fragment
    ))

    return safe_url

# ----------------------------------------------------------------------
# Example usage (uncomment for testing):
#
# try:
#     safe = verify_webhook("https://api.example.com/webhook/notify")
#     print(f"Safe URL: {safe}")
# except ValueError as e:
#     print(f"Validation failed: {e}")