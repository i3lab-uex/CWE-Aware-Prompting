import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.org",
    "public.api.net",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),      # loopback
    ipaddress.ip_network("169.254.0.0/16"),   # link-local
    ipaddress.ip_network("::1/128"),         # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),       # IPv6 link-local
]

def _is_private_ip(host: str) -> bool:
    """
    Return True if the given host resolves to a private IP address.
    If the host is not an IP, we assume it is safe (DNS will resolve later).
    """
    try:
        # Check if host is a literal IP address
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP literal; assume it's a hostname
        return False

    for network in PRIVATE_IP_RANGES:
        if ip in network:
            return True
    return False


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate and sanitize a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_address : str
        The raw URL received from the external service.

    Returns
    -------
    str
        A fully qualified, validated URL that can safely be used for an internal API request.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved domain, or points to a private/internal network.
    """
    # Parse the URL
    parsed = urlparse(webhook_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain scheme and host")

    # Normalize the domain to lower case for comparison
    netloc = parsed.netloc.split(":")[0].lower()

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(netloc):
        raise ValueError("URL resolves to a private IP address")

    # Validate domain against the whitelist
    if netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not an approved API endpoint")

    # Rebuild the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragment is removed for security
    ))

    return sanitized