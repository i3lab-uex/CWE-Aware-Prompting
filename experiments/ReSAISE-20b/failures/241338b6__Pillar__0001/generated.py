import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelisted domains (add approved external APIs here)
APPROVED_DOMAINS = {
    "api.github.com",
    "api.openai.com",
    "data.example.com",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3}) |
        # localhost
        (127\.0\.0\.1)
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private range."""
    return PRIVATE_IP_RE.match(ip) is not None

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all its IP addresses."""
    try:
        return socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that the supplied URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves to a private IP.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_check)

    # Basic URL sanity checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url_to_check}")

    # Ensure HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Check against the whitelist
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve the host and ensure no private IPs are returned
    addr_info = _resolve_host(host)
    if not addr_info:
        raise ValueError(f"Could not resolve host: {host}")

    for entry in addr_info:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Host {host} resolves to private IP {ip}")

    # Reconstruct the URL to ensure it is in a canonical form
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized