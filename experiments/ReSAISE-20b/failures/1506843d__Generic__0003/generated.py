import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a whitelist of trusted API domains.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.provider.net",
}

# Define a set of disallowed IP networks (private, loopback, link-local, etc.)
DISALLOWED_IP_RANGES = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),        # IPv6 link-local
]

def _is_ip_disallowed(ip: str) -> bool:
    """
    Return True if the given IP string falls into a disallowed network.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # If it cannot be parsed as an IP, assume it's not a numeric address
        return False

    for net in DISALLOWED_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return socket.gethostbyname_ex(hostname)[2]

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, unchanged if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a disallowed domain/IP,
        or attempts to access an internal/private network.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    # Basic parsing
    parsed = urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url_to_inspect}")

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 1. Check against the trusted domain whitelist
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted domains")

    # 2. Resolve hostname to IPs and ensure none are disallowed
    try:
        ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc

    for ip in ips:
        if _is_ip_disallowed(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to disallowed IP {ip}")

    # 3. Reconstruct the URL (normalise) and return
    cleaned = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return cleaned