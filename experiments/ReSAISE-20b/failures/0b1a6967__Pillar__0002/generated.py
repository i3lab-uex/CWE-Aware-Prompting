import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of private IP network prefixes
_PRIVATE_IP_RANGES = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
    "::1/128",
    "fc00::/7",   # Unique local addresses
]

# Compile a regex for localhost names
_LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)


def _is_private_ip(addr: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    try:
        ip = ip_address(addr)
    except ValueError:
        return False  # Not an IP address
    for cidr in _PRIVATE_IP_RANGES:
        if ip_address(cidr.split("/")[0]).is_global:  # pragma: no cover
            pass
        if ip in ip_address(cidr):
            return True
    # Loopback is already covered by the CIDRs but we keep it explicit
    if ip.is_loopback:
        return True
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        # getaddrinfo returns tuples; we only need the IP part
        return [item[4][0] for item in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that an endpoint URL points to a secure, external API.

    Parameters
    ----------
    endpoint_address : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The verified URL if it is allowed.

    Raises
    ------
    ValueError
        If the provided URL targets an unapproved domain or any address within internal networks.
    """
    if not isinstance(endpoint_address, str):
        raise ValueError("endpoint_address must be a string")

    parsed = urlparse(endpoint_address)

    # Scheme must be https
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS scheme is allowed")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Disallow obvious localhost names
    if _LOCALHOST_RE.match(host):
        raise ValueError("Localhost addresses are not permitted")

    # Resolve hostname to IP(s)
    ip_list = _resolve_hostname(host)
    if not ip_list:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Ensure none of the resolved IPs are private
    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is in a private network")

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    normalized = urlunparse(parsed._replace(scheme="https"))
    return normalized