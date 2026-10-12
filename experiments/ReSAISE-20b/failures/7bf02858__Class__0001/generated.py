import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API hostnames or domain patterns (regex)
APPROVED_HOST_PATTERNS = [
    r"^api\.example\.com$",
    r"^public-api\.service\.org$",
]

# List of approved domain suffixes
APPROVED_DOMAIN_SUFFIXES = [
    ".example.com",
    ".service.org",
]

# Private IP networks that must be rejected
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is within a private network."""
    addr = ipaddress.ip_address(ip)
    return any(addr in net for net in PRIVATE_NETWORKS)

def _is_approved_host(host: str) -> bool:
    """Check if host matches approved patterns or suffixes."""
    for pattern in APPROVED_HOST_PATTERNS:
        if re.match(pattern, host):
            return True
    for suffix in APPROVED_DOMAIN_SUFFIXES:
        if host.endswith(suffix):
            return True
    return False

def _resolve_and_validate(host: str) -> None:
    """Resolve host to IP and ensure it is not private."""
    try:
        # Resolve all addresses for the host
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Host '{host}' resolves to private IP {ip}, which is disallowed")

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL before it is used to call an internal API.

    Parameters
    ----------
    hook_url : str
        The URL provided by the external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints or
        resolves to an internal network location.
    """
    if not hook_url:
        raise ValueError("hook_url must be a non-empty string")

    parsed = urlparse(hook_url)

    # Enforce HTTPS or HTTP only
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'")

    # Ensure the host part exists
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # Reject any IP address hosts directly
    try:
        ipaddress.ip_address(host)
        raise ValueError("Direct IP addresses are not allowed in the URL")
    except ValueError:
        pass  # Not an IP literal, continue

    # Validate host against approved patterns/suffixes
    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not in the list of approved domains")

    # Resolve host to ensure it doesn't point to a private network
    _resolve_and_validate(host)

    # Reconstruct the URL to ensure normalization (strip fragments, etc.)
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{parsed.hostname}{':' + str(parsed.port) if parsed.port else ''}",
            parsed.path or "/",
            "",  # params
            parsed.query,
            "",  # fragment
        )
    )

    return safe_url