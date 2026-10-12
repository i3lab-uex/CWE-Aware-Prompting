import re
import socket
from urllib.parse import urlparse

# Regular expression to detect private IP ranges, RFC1918 addresses and loopback
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.)|                      # Loopback
    (^10\. )|                      # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\. ) |# Class B private
    (^192\.168\. )|                # Class C private
    (^169\.254\.)|                 # Link-local
    (^0\.0\.0\.0$)                 # Unspecified
    """,
    re.VERBOSE,
)

# RFC 6890: Reserved IP ranges that should not be reachable from the public internet
RESERVED_IPS = [
    ("192.0.2.", 8),   # TEST-NET-1
    ("198.51.100.", 8),# TEST-NET-2
    ("203.0.113.", 8), # TEST-NET-3
]

def _is_ip_in_reserved_range(ip: str) -> bool:
    """Check if an IP belongs to a reserved test network."""
    for prefix, bits in RESERVED_IPS:
        if ip.startswith(prefix):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, link‑local or otherwise disallowed."""
    # Simple regex for quick checks
    if PRIVATE_IP_REGEX.search(ip):
        return True

    # Additional check for IPv6 privacy ranges
    if ip.lower().startswith("fc") or ip.lower().startswith("fd"):
        return True

    # Reserved IPv6 addresses
    if ip.lower() in ("::1", "fe80::", "ff00::"):
        return True

    # Reserved test networks
    if _is_ip_in_reserved_range(ip):
        return True

    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that a given URL is safe to access as an external API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an unsafe scheme, targets a private/internal IP,
        or resolves to any disallowed address.
    """
    # Basic scheme validation
    parsed = urlparse(endpoint_address)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname or IP address.")

    # Resolve the hostname to all associated IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{parsed.hostname}': {exc}") from exc

    # Ensure none of the resolved addresses are disallowed
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Disallowed IP address resolved for host '{parsed.hostname}': {ip}")

    # Reconstruct the URL with a cleaned netloc (no userinfo or port)
    netloc = parsed.hostname
    if parsed.port:
        netloc += f":{parsed.port}"
    cleaned = parsed._replace(netloc=netloc, username=None, password=None)

    return cleaned.geturl()