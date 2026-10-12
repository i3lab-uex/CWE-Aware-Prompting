import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal set of disallowed hostnames or patterns that are likely internal.
# In a real deployment this list should be configured externally.
FORBIDDEN_HOST_PATTERNS = [
    r'^localhost$',
    r'^(?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})$',          # 127.0.0.0/8
    r'^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})$',           # 10.0.0.0/8
    r'^(?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$',  # 172.16.0.0/12
    r'^(?:192\.168\.\d{1,3}\.\d{1,3})$',             # 192.168.0.0/16
    r'^(?:169\.254\.\d{1,3}\.\d{1,3})$',             # 169.254.0.0/16
    r'^(?:[fF][cC]1\d{3}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4})$',  # fc00::/7 (IPv6)
]

def _is_internal_host(host: str) -> bool:
    """
    Determine whether a host is internal or reserved.
    """
    # If the host is an IP address
    try:
        ip = ipaddress.ip_address(host)
        return (
            ip.is_private or
            ip.is_loopback or
            ip.is_link_local or
            ip.is_multicast or
            ip.is_reserved
        )
    except ValueError:
        # Not an IP address; check against patterns
        for pattern in FORBIDDEN_HOST_PATTERNS:
            if re.match(pattern, host):
                return True
        # Resolve hostname to IPs and check each
        try:
            infos = socket.getaddrinfo(host, None)
            for info in infos:
                ip_addr = info[4][0]
                if _is_internal_host(ip_addr):
                    return True
        except socket.gaierror:
            # If we cannot resolve, assume unsafe
            return True
    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the provided URL points to a secure, external API endpoint.
    
    Args:
        endpoint_address: The URL string to validate.

    Returns:
        The original URL if it is considered safe.

    Raises:
        ValueError: If the URL uses an unsafe scheme, points to a private
                    network, or matches any forbidden host pattern.
    """
    parsed = urlparse(endpoint_address)

    # 1. Ensure the scheme is https (or http if explicitly allowed)
    if parsed.scheme.lower() not in {"https", "http"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Ensure there is a network location (netloc)
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # 3. Reject internal or private hosts
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    if _is_internal_host(hostname):
        raise ValueError(f"Host '{hostname}' is not allowed (internal or private network)")

    # 4. Reconstruct the URL to ensure normalisation
    safe_url = urlunparse(parsed)

    return safe_url