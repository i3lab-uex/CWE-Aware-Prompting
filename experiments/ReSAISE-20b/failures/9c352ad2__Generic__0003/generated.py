import re
from urllib.parse import urlparse

# List of approved public API domains (example entries)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.publicapi.org",
    "data.partner.net"
}

# Regex patterns to detect private/internal IP addresses
PRIVATE_IP_PATTERNS = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^::1$"),  # IPv6 loopback
]

def is_private_ip(host: str) -> bool:
    """
    Return True if host is a private or loopback IP address.
    """
    # Direct IPv4/IPv6 numeric match
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True

    # Try to interpret as IP (both IPv4 and IPv6)
    try:
        import ipaddress
        return ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback
    except ValueError:
        # Not an IP address; fallback to hostname checks
        return False

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved public API.
    
    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.
    
    Returns
    -------
    str
        The validated URL pointing to a pre-approved API endpoint.
    
    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it resolves to a private/internal address.
    """
    parsed = urlparse(webhook_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private or loopback IPs
    if is_private_ip(host):
        raise ValueError("URL points to a private or internal IP address")

    # Reject hostnames that are not in the approved domain list
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # All checks passed; return the original URL
    return webhook_url