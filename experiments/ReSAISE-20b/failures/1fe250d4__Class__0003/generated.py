import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A list of domains that are explicitly allowed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

# Regular expression to detect URLs that start with http:// or https://
_URL_RE = re.compile(r"^(https?://)", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address string is part of a private, reserved,
    or otherwise non‑public network.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
        )
    except ValueError:
        # If the string is not a valid IP address, treat it as non‑private.
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    Return an empty list if resolution fails.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []

    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)


def _is_allowed_domain(host: str) -> bool:
    """
    Return True if the host is exactly in the ALLOWED_DOMAINS set.
    The comparison is case‑insensitive.
    """
    return host.lower() in ALLOWED_DOMAINS


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to a secure, external API endpoint.

    The function performs the following checks:
        1. Must use http:// or https://.
        2. Host must be in the ALLOWED_DOMAINS list.
        3. All resolved IP addresses for the host must be public (non‑private).

    Parameters
    ----------
    endpoint_url : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain, or resolves to any
        internal/private IP address.
    """
    # Basic scheme check
    if not _URL_RE.match(endpoint_url):
        raise ValueError("Only http:// and https:// URLs are allowed")

    parsed = urlparse(endpoint_url)

    # Ensure a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Domain whitelist
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the whitelist")

    # Resolve host to IPs and verify none are private
    ips = _resolve_hostname(parsed.hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {parsed.hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for host {parsed.hostname} is private")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return safe_url