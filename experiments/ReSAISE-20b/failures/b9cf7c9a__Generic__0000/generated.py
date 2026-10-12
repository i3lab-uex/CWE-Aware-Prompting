import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelist of approved external API domains (add as needed)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.example.com",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 169.254.0.0 – 169.254.255.255 (link-local)
        (169\.254\.\d{1,3}\.\d{1,3})
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all its IPv4 addresses."""
    try:
        infos = socket.getaddrinfo(host, None, family=socket.AF_INET)
        return [sock[4][0] for sock in infos]
    except socket.gaierror:
        return []

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to be validated.

    Returns
    -------
    str
        A normalized URL that has been confirmed to point to an approved external API.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not belong to an approved domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    parsed = urlparse(endpoint_url)

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Hostname extraction
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Domain whitelist check (case-insensitive)
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not in the approved domains list")

    # Resolve hostname to IP addresses
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Check each IP against private ranges
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP address: {ip}")

    # Reconstruct the URL in canonical form
    normalized = urlunparse(
        (
            parsed.scheme.lower(),
            f"{host}:{parsed.port}" if parsed.port else host,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized