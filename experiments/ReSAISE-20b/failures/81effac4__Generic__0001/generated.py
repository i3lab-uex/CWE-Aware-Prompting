import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are allowed to be called from the application.
# Add or remove trusted hosts as needed for your environment.
TRUSTED_DOMAINS = {
    "api.example.com",
    "trusted.api.org",
    "service.internal.company.com",
}

# Private and reserved IP networks that should never be accessed.
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),        # link-local IPv6
    ipaddress.ip_network("fc00::/7"),         # unique local (ULA)
]

def _is_ip_allowed(ip: str) -> bool:
    """Return True if the IP is not private or reserved."""
    addr = ipaddress.ip_address(ip)
    for net in _PRIVATE_NETWORKS:
        if addr in net:
            return False
    # Exclude multicast and any other non-public ranges as needed.
    if addr.is_multicast or addr.is_reserved:
        return False
    return True

def _is_trusted_domain(hostname: str) -> bool:
    """Return True if hostname is in the list of trusted domains."""
    # Normalize to lowercase and strip trailing dot.
    host = hostname.lower().rstrip('.')
    if host in TRUSTED_DOMAINS:
        return True
    # Allow subdomains of trusted domains.
    for domain in TRUSTED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False

def check_api_link(api_link: str) -> str:
    """
    Validate an API URL ensuring it points to a trusted external service.
    
    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a private/internal IP address, or its hostname
        is not in the list of trusted domains.
    """
    # Basic parsing and scheme validation.
    parsed = urlparse(api_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to IP addresses.
    try:
        addrinfo = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname {parsed.hostname!r}") from exc

    # Ensure every resolved IP is allowed and the domain is trusted.
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if not _is_ip_allowed(ip):
            raise ValueError(f"IP address {ip} is private or reserved")
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Hostname {parsed.hostname!r} is not trusted")

    # Reconstruct the URL to ensure it hasn't been tampered with.
    safe_url = urlunparse(parsed)
    return safe_url