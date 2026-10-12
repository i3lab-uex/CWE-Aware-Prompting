import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted for API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "auth.secure.net",
}

# Private and link-local IP ranges that must be rejected.
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # Unique local addresses
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is within a private or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for network in PRIVATE_IP_RANGES:
        if addr in network:
            return True
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the hostname, or raise if resolution fails."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc
    ips = {info[4][0] for info in infos}
    return list(ips)


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API and does not target
    internal or sensitive network addresses.

    Parameters:
        url_to_inspect (str): The URL to be validated.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    targets an untrusted domain, or resolves to a private IP.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_inspect)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname.")

    # Normalize hostname for comparison
    host = parsed.hostname.lower()

    # Check if the domain is in the trusted list (exact match or subdomain)
    if not any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains.")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(host)

    # Reject if any resolved IP is private or local
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP address {ip} which is disallowed.")

    # Reconstruct the URL to ensure it is normalized
    cleaned = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return cleaned