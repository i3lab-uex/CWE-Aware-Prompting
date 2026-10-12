import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Define a whitelist of approved domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.internal.net",
}

# Regular expression for detecting IP addresses in a hostname
IP_REGEX = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6 (simplified)
        \[([0-9a-fA-F:]+)\]
    )
    $
""", re.VERBOSE)


def _is_internal_ip(ip: str) -> bool:
    """Return True if the IP is part of a private, loopback or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False


def _is_allowed_domain(host: str) -> bool:
    """Check if host is in the allowed domain whitelist."""
    # Normalize: strip port and compare lowercased
    host = host.split(":")[0].lower()
    return host in ALLOWED_DOMAINS


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the given URL points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_url : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The verified URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain or any address within internal networks.
    """
    if not endpoint_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(endpoint_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Resolve the hostname to all IP addresses
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # Check each resolved IP
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_internal_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to internal IP {ip}")

    # Ensure host is in the whitelist
    if not _is_allowed_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the approved domain list")

    # Reconstruct the URL to normalize it
    verified_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return verified_url