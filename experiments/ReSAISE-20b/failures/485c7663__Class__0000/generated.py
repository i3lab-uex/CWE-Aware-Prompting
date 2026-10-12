import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are explicitly allowed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.company.org",
    "trusted.api.net",
}

# Private IP networks that must be blocked.
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # Unique local address
]

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback network."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for net in PRIVATE_NETWORKS:
        if ip_obj in net:
            return True
    return False

def _resolve_and_check(host: str) -> None:
    """
    Resolve the hostname to all IPv4/IPv6 addresses and raise
    ValueError if any resolved IP is private.
    """
    try:
        # Resolve both IPv4 and IPv6 addresses
        for result in socket.getaddrinfo(host, None):
            ip = result[4][0]
            if _is_ip_private(ip):
                raise ValueError(f"Resolved IP {ip} for host '{host}' is private or loopback.")
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied URL points to an approved external API endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, verified URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        points to an unapproved domain or resolves to a private IP.
    """
    # Parse and validate scheme
    parsed = urlparse(api_endpoint)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Disallow IP literals that are private
    try:
        ipaddress.ip_address(host)
        if _is_ip_private(host):
            raise ValueError(f"IP address '{host}' is private or loopback.")
    except ValueError:
        # Not an IP literal; treat as hostname
        pass

    # Domain whitelist check (case-insensitive)
    if host.lower() not in {d.lower() for d in ALLOWED_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not in the list of approved domains.")

    # Resolve hostname to ensure it doesn't point to a private IP
    _resolve_and_check(host)

    # Reconstruct the URL (normalizing components)
    cleaned = urlunparse((
        parsed.scheme.lower(),
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return cleaned