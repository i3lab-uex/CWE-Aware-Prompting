import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved domains (can be expanded)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "openapi.safe.io",
}

# Regular expression to detect URLs that are not fully qualified
VALID_URL_RE = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private, loopback, link-local or reserved."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return True


def _resolve_host(host: str) -> list[str]:
    """Resolve the host to a list of IP addresses."""
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve host: {host}")

    ips = []
    for info in infos:
        ip = info[4][0]
        if not _is_private_ip(ip):
            ips.append(ip)
    return ips


def validate_service_url(service_url: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated and normalized URL.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it resolves to a private/internal IP.
    """
    # Basic syntax check
    match = VALID_URL_RE.match(service_url)
    if not match:
        raise ValueError(f"Invalid URL format: {service_url}")

    scheme = match.group("scheme").lower()
    host = match.group("host")
    path = match.group("path") or ""

    # Normalize the host (strip port if present)
    host_parts = host.split(":")
    hostname = host_parts[0].lower()

    # Ensure domain is approved
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve the hostname and check for private IPs
    resolved_ips = _resolve_host(hostname)
    if not resolved_ips:
        raise ValueError(f"Resolved IPs for '{hostname}' are private or unreachable")

    # Reconstruct the URL to ensure consistency
    normalized_url = urlunparse((scheme, host, path, "", "", ""))
    return normalized_url