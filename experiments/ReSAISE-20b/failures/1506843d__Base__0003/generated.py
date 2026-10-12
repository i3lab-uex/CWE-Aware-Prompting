import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "data.provider.net",
}

# Regular expression to quickly reject obvious localhost or private IP patterns.
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)

# IPv4 and IPv6 private address blocks
PRIVATE_IPV4_BLOCKS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
]
PRIVATE_IPV6_BLOCKS = [
    ipaddress.IPv6Network("fc00::/7"),
    ipaddress.IPv6Network("fe80::/10"),
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return True  # invalid IPs are treated as unsafe
    if ip_obj.is_loopback or ip_obj.is_reserved:
        return True
    for net in PRIVATE_IPV4_BLOCKS + PRIVATE_IPV6_BLOCKS:
        if ip_obj in net:
            return True
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of resolved IP addresses for the given hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []
    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The validated URL (unchanged if validation passes).

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain, resolves to a private IP,
        or attempts to access internal/sensitive network locations.
    """
    # Parse the URL
    parsed = urlparse(url_to_inspect)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious localhost references
    if LOCALHOST_RE.match(hostname):
        raise ValueError("URL points to localhost, which is disallowed")

    # Resolve hostname to IPs and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")

    # Ensure the hostname is within the list of trusted domains
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {hostname} is not a trusted domain")

    # Reconstruct the URL to ensure consistency
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned