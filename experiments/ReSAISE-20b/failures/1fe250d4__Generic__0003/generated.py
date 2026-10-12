import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of allowed external domains (regex patterns or exact strings)
ALLOWED_DOMAINS = [
    r"^api\.example\.com$",
    r"^services\.trustedpartner\.org$",
    # Add more allowed domains here
]

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|"
    r"fc00:|fd00:)"  # IPv6 unique local addresses
)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    try:
        ip = ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _is_allowed_domain(host: str) -> bool:
    """Check if the host matches any of the allowed domain patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, host):
            return True
    return False


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to a list of IP addresses."""
    try:
        return [
            addr[4][0]
            for addr in socket.getaddrinfo(host, None)
        ]
    except socket.gaierror:
        return []


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that a given URL points to an allowed external API endpoint.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated and normalized URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, points to a private/internal IP,
        or does not resolve to an approved domain.
    """
    # Parse the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against allowed domain patterns
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain {host!r} is not in the allowed list")

    # Resolve hostname to IP addresses and ensure none are private
    resolved_ips = _resolve_host(host)
    if not resolved_ips:
        raise ValueError(f"Unable to resolve host: {host!r}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip!r} for host {host!r} is private or internal")

    # Reconstruct the URL to ensure consistent formatting
    normalized_url = urlunparse(parsed._replace(netloc=f"{host}:{parsed.port or ''}".strip(':')))
    return normalized_url