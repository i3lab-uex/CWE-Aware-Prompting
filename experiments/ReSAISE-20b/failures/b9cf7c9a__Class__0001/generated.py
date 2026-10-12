import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved external API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "services.example.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # ::1 (IPv6 loopback)
        (::1)|
        # IPv6 link-local
        (fe80:(?:[0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})|
        # IPv6 unique local address
        (fc00:(?:[0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})|
        # IPv6 privacy extensions
        (fd00:(?:[0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to a list of IP addresses."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to an approved external API.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        A normalised URL that has been confirmed to belong to an approved domain.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves to a private/internal address.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    parsed = urlparse(endpoint_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise the hostname to lowercase for domain comparison
    host_lower = host.lower()

    if host_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve hostname to IP addresses and check for private ranges
    addrinfo = _resolve_hostname(host)
    if not addrinfo:
        raise ValueError(f"Could not resolve hostname: {host}")

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP: {ip}")

    # Re‑build the URL with normalised components (e.g., no trailing slash)
    normalized = urlunparse(
        (
            parsed.scheme,
            host_lower + (f":{parsed.port}" if parsed.port else ""),
            parsed.path.rstrip("/"),
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized