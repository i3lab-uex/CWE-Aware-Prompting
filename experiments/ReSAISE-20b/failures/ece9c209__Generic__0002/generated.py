import re
import socket
from urllib.parse import urlparse

# List of allowed API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.trusted.io",
    "data.partner.org",
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|              # 10.0.0.0/8
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})| # 172.16.0.0/12
        (?:192\.168\.\d{1,3}\.\d{1,3})|                 # 192.168.0.0/16
        (?:169\.254\.\d{1,3}\.\d{1,3})|                 # 169.254.0.0/16 (link-local)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|             # 127.0.0.0/8 (loopback)
        (?:0\.0\.0\.0)                                 # 0.0.0.0
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str):
    """Resolve hostname to a list of IP addresses."""
    try:
        # getaddrinfo returns tuples: (family, type, proto, canonname, sockaddr)
        return [sockaddr[0] for _, _, _, _, sockaddr in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to a trusted external API endpoint.

    Raises:
        ValueError: If the URL is malformed, points to a private address,
                    or not in ALLOWED_DOMAINS.
    Returns:
        The validated URL string (unchanged if valid).
    """
    # Basic URL parsing
    parsed = urlparse(api_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Reject non-HTTPS URLs (optional but recommended)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for API endpoints")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Hostname could not be determined")

    # Check against allowed domains
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the list of allowed domains")

    # Resolve hostname to IPs and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # All checks passed
    return api_url