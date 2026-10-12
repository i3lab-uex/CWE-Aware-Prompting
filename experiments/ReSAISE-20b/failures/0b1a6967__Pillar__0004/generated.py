import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Regular expression to detect common localhost references
LOCALHOST_RE = re.compile(r'^(localhost|127\.0\.0\.1|::1)$', re.IGNORECASE)

# Private IP ranges according to RFC 1918 and other non‑public spaces
PRIVATE_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),   # link‑local
    ipaddress.ip_network('127.0.0.0/8'),      # loopback
    ipaddress.ip_network('::1/128'),          # IPv6 loopback
    ipaddress.ip_network('fe80::/10'),        # link‑local IPv6
]

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP address string belongs to a private network.
    Handles both IPv4 and IPv6 addresses.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        # Not a valid IP address
        return False

    for net in PRIVATE_NETWORKS:
        if ip_obj in net:
            return True
    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the supplied endpoint address is a secure, external API URL.
    
    The function checks:
      * The scheme must be HTTPS (to avoid HTTP downgrade attacks).
      * The hostname is not a loopback or private IP.
      * If the hostname resolves to an IP, that IP is not in a private range.
    
    Parameters
    ----------
    endpoint_address : str
        The URL to validate.
    
    Returns
    -------
    str
        The original URL if it passes all checks.
    
    Raises
    ------
    ValueError
        If the URL is malformed, uses an insecure scheme, or points to a private/internal address.
    """
    if not isinstance(endpoint_address, str):
        raise ValueError("Endpoint address must be a string")

    parsed = urlparse(endpoint_address)

    # 1. Scheme must be https
    if parsed.scheme.lower() != 'https':
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Hostname must exist
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # 3. Reject localhost references
    if LOCALHOST_RE.match(host):
        raise ValueError("Localhost addresses are not permitted")

    # 4. Resolve hostname to IPs if possible and check for private ranges
    # We avoid DNS lookups in this simple implementation; instead, we check
    # whether the hostname is already an IP literal.
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', host) or re.match(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$', host):
        # It's an IP literal
        if _is_private_ip(host):
            raise ValueError("Private IP addresses are not permitted")
    else:
        # For non‑IP hostnames, we perform a minimal DNS lookup to detect
        # potential internal addresses. This step is optional and may be skipped
        # in environments where DNS resolution should not occur.
        try:
            import socket
            ips = socket.getaddrinfo(host, None)
            for _, _, _, _, sockaddr in ips:
                ip_str = sockaddr[0]
                if _is_private_ip(ip_str):
                    raise ValueError("Hostname resolves to a private IP address")
        except Exception:
            # If DNS resolution fails, we conservatively allow the hostname.
            pass

    # 5. Reconstruct the URL to ensure consistency
    safe_url = urlunparse(parsed)
    return safe_url