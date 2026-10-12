import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Define a whitelist of allowed hostnames (exact match or suffix)
ALLOWED_DOMAINS = [
    "api.example.com",
    "service.internal.org",
]

# Define CIDR blocks that are considered internal/unsafe
UNSAFE_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("224.0.0.0/4"),   # multicast
]

def _is_ip_in_unsafe_network(ip: str) -> bool:
    """Check if an IP string belongs to a known unsafe network."""
    ip_obj = ipaddress.ip_address(ip)
    return any(ip_obj in net for net in UNSAFE_NETWORKS)

def _is_domain_allowed(hostname: str) -> bool:
    """Check if the hostname matches one of the allowed domains."""
    for domain in ALLOWED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that the provided URL points to an approved external API endpoint.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL resolves to an unapproved domain or an internal/private IP.
    """
    # Parse and normalise the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {endpoint_url}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Unable to extract host from URL: {endpoint_url}")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {hostname}: {exc}") from exc

    # Check each resolved IP
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_ip_in_unsafe_network(ip):
            raise ValueError(f"Resolved IP {ip} for host {hostname} is in an unsafe network.")
        if not _is_domain_allowed(hostname):
            raise ValueError(f"Host {hostname} is not in the allowed domain list.")

    # Rebuild the URL to ensure no hidden components (e.g., port spoofing)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return safe_url