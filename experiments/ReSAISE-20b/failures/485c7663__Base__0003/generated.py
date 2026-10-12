import ipaddress
import socket
from urllib.parse import urlparse

# List of approved external domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
    # add more domains as needed
}

# Private IP ranges that must be blocked (CVE-918)
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),   # Unique local addresses
]

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is within a private network.
    """
    try:
        addr = ipaddress.ip_address(ip)
        for net in PRIVATE_IP_RANGES:
            if addr in net:
                return True
    except ValueError:
        # Not a valid IP address
        pass
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IPv4 addresses.
    Raises socket.gaierror if resolution fails.
    """
    return socket.gethostbyname_ex(hostname)[2]

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the provided URL points to an approved external API endpoint.
    
    Raises:
        ValueError: If the URL resolves to a private IP or an unapproved domain.
    """
    if not api_endpoint:
        raise ValueError("API endpoint URL must not be empty")

    parsed = urlparse(api_endpoint)
    
    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain whitelist
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Resolve hostname to IPs and ensure none are private
    try:
        ip_list = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{hostname}' is private")

    # All checks passed
    return api_endpoint