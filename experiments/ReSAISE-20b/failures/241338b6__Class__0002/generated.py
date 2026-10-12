import re
import socket
import ipaddress
from urllib.parse import urlparse

# List of approved domains (regex patterns or plain strings)
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^data\.trustedsource\.org$",
    r"^services\.secureapi\.net$",
]

# Compile regex patterns for quick matching
APPROVED_REGEX = [re.compile(pattern) for pattern in APPROVED_DOMAINS]


def _is_approved_domain(host: str) -> bool:
    """
    Return True if the host matches one of the approved domain patterns.
    """
    for regex in APPROVED_REGEX:
        if regex.match(host.lower()):
            return True
    return False


def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is public (i.e., not private, loopback,
    link-local, or reserved).
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    # Exclude private, loopback, link-local, multicast and reserved addresses
    return not (
        addr.is_private or
        addr.is_loopback or
        addr.is_link_local or
        addr.is_multicast or
        addr.is_reserved
    )


def _resolve_host_to_public_ip(host: str) -> str:
    """
    Resolve the host to an IP address and ensure it is public.
    Raises ValueError if resolution fails or the IP is non‑public.
    """
    try:
        # Resolve all A records; pick the first public one
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_public_ip(ip):
            return ip

    raise ValueError(f"All resolved IPs for host '{host}' are non‑public.")


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is approved and safe.

    Raises
    ------
    ValueError
        If the URL does not use http/https, targets an unapproved domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_check)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 1. Domain whitelist check
    if not _is_approved_domain(host):
        raise ValueError(f"Host '{host}' is not in the approved domain list")

    # 2. Resolve to IP and ensure it's public
    _resolve_host_to_public_ip(host)

    # 3. Return the URL unchanged if all checks pass
    return url_to_check