import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of CIDR blocks that represent private or reserved addresses.
_PRIVATE_CIDRS = [
    ipaddress.ip_network("0.0.0.0/8"),      # RFC 1918 & unspecified
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),     # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),        # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),      # IPv6 link-local
    ipaddress.ip_network("fc00::/7")        # IPv6 unique local
]

# Regex to detect IPv4 literals.
_IPV4_REGEX = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
# Regex to detect IPv6 literals (simple check).
_IPV6_REGEX = re.compile(r"^\[?[0-9a-fA-F:]+\.?\]?$")

def _is_private_ip(ip_addr: str) -> bool:
    """
    Returns True if the IP address is within a private or reserved range.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_addr)
        for cidr in _PRIVATE_CIDRS:
            if ip_obj in cidr:
                return True
        return False
    except ValueError:
        # Not a valid IP address.
        return False

def _resolve_host_to_ips(host: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.
    """
    try:
        # getaddrinfo returns (family, type, proto, canonname, sockaddr)
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {host}")

    ips = set()
    for info in infos:
        sockaddr = info[4]
        ip = sockaddr[0]  # IPv4 or IPv6 address string
        ips.add(ip)
    return list(ips)

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the supplied URL points to a secure, external API endpoint.

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
        raise ValueError("Endpoint address must be a string")

    parsed = urlparse(endpoint_address)

    # Scheme must be HTTPS.
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # No userinfo in the URL.
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain user credentials")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Detect IP literals directly in the host part.
    if _IPV4_REGEX.match(host) or _IPV6_REGEX.match(host):
        # Direct IP address
        if _is_private_ip(host):
            raise ValueError(f"IP address {host} is private or reserved")
        return endpoint_address

    # Resolve hostname to IP addresses and ensure none are private.
    ips = _resolve_host_to_ips(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {host} resolves to private IP {ip}")

    # If we reach here, the URL is considered safe.
    return endpoint_address