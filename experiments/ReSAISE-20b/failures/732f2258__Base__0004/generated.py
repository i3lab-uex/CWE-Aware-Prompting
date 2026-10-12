import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private or reserved address."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If IP is not resolvable as an IP address, treat it as safe
        return False

def _validate_domain(domain: str) -> None:
    """Validate that the domain is in the allowed list."""
    if domain.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not in the allowed list.")

def _ensure_not_private_ip(host: str) -> None:
    """Resolve host to IP(s) and ensure none are private."""
    try:
        for addr in socket.getaddrinfo(host, None):
            ip = addr[4][0]
            if _is_private_ip(ip):
                raise ValueError(f"Host '{host}' resolves to private IP '{ip}'.")
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve host '{host}': {e}")

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL against an approved domain list and
    ensure it does not point to a private/internal network.

    Parameters:
        webhook_address (str): The URL supplied by an external service.

    Returns:
        str: A sanitized, validated URL safe for internal use.

    Raises:
        ValueError: If the domain is not allowed or resolves to a private IP.
    """
    # Basic URL parsing
    parsed = urlparse(webhook_address)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format.")

    # Strip any userinfo and port for domain validation
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Validate domain against whitelist
    _validate_domain(host)

    # Resolve host and check for private IPs
    _ensure_not_private_ip(host)

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "", "",
         parsed.query or "", parsed.fragment or "")
    )
    return sanitized