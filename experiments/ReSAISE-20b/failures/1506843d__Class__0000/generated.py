import socket
import urllib.parse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of domains that are considered trusted.  Add any additional
# third‑party API hosts here.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
    # Add more as needed
}

# Private, loopback and link‑local address blocks (RFC 1918 + others)
_PRIVATE_NETWORKS = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),
    ("169.254.0.0", "169.254.255.255"),
    ("::1/128"),               # IPv6 loopback
    ("fc00::/7"),              # Unique local address (ULA)
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is within a private or
    otherwise restricted network block."""
    addr = ip_address(ip)

    for net in _PRIVATE_NETWORKS:
        if isinstance(net, tuple):
            start = ip_address(net[0])
            end = ip_address(net[1])
            if start <= addr <= end:
                return True
        else:  # CIDR notation
            if addr in ip_address(net):
                return True

    return False

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that `url_to_inspect` points to an external, trusted API
    endpoint and does not resolve to a private or internal IP address.
    
    Parameters
    ----------
    url_to_inspect : str
        The API URL to be verified.
    
    Returns
    -------
    str
        The validated URL, unchanged from the input if it passes checks.
    
    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or resolves to an
        internal/private IP address.
    """
    # Basic URL parsing
    parsed = urllib.parse.urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url_to_inspect}")

    host = parsed.hostname
    if not host:
        raise ValueError(f"URL must contain a hostname: {url_to_inspect}")

    # Ensure the host is in the trusted domain list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve the hostname to all IP addresses (IPv4 & IPv6)
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # Check that none of the resolved addresses are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Host '{host}' resolves to private IP {ip}")

    # All checks passed – return the original URL
    return url_to_inspect