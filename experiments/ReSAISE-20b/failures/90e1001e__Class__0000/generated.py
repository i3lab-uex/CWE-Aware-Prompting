import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains.  Add or remove as needed.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "data.provider.net"
}

# Regular expression to detect common internal IP patterns
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0/8 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 link-local
        ([a-fA-F0-9:]+::1)
    )
    """,
    re.VERBOSE
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or link‑local."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all IPv4/IPv6 addresses."""
    try:
        # getaddrinfo returns tuples; the 4th element is sockaddr, index 0 holds IP
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from None
    return [info[4][0] for info in infos]

def validate_service_url(service_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves to a private/internal address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: '{service_url}'")

    # Ensure HTTPS to mitigate downgrade attacks
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Only HTTPS URLs are allowed, got scheme '{parsed.scheme}'")

    host = parsed.hostname
    if not host:
        raise ValueError(f"URL does not contain a valid hostname: '{service_url}'")

    # Check domain is approved
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve hostname and ensure no private IPs are returned
    addresses = _resolve_host(host)
    for ip in addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private/internal")

    # Optionally, we could check that the resolved IPs are not blacklisted
    # or perform certificate validation, but this is beyond scope.

    # Reconstruct the URL to ensure it remains canonical
    safe_url = urlunparse(parsed._replace(scheme="https"))
    return safe_url