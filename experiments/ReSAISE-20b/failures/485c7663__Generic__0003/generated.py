import re
from urllib.parse import urlparse, unquote
import socket
import ipaddress

# Whitelisted domains or domain patterns (regex)
WHITELISTED_DOMAINS = [
    r'^api\.example\.com$',
    r'^services\.trusted\.org$',
    r'^external\.domain\.net$',          # exact match
]

# Internal IP ranges to block
INTERNAL_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),   # loopback
    ipaddress.ip_network('::1/128'),      # IPv6 loopback
]

def _is_ip_internal(ip: str) -> bool:
    """Return True if the IP address is within any internal network."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False  # Not a valid IP, will be handled elsewhere
    for net in INTERNAL_IP_RANGES:
        if ip_obj in net:
            return True
    return False

def _resolve_host_to_ip(host: str) -> list[str]:
    """Resolve a hostname to all its IP addresses."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror:
        # Unable to resolve; treat as disallowed
        return []

def _matches_whitelist(host: str) -> bool:
    """Check if host matches any whitelist regex."""
    for pattern in WHITELISTED_DOMAINS:
        if re.match(pattern, host, flags=re.IGNORECASE):
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the provided URL points to an approved external API endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL points to an unapproved domain or any internal network address.
    """
    # Parse and validate scheme
    parsed = urlparse(api_endpoint)
    if parsed.scheme not in {'http', 'https'}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Decode percent-encoded host
    host = unquote(parsed.hostname or '')
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Whitelist check
    if not _matches_whitelist(host):
        raise ValueError(f"Domain '{host}' is not in the whitelist.")

    # Resolve host to IP addresses
    ip_list = _resolve_host_to_ip(host)
    if not ip_list:
        raise ValueError(f"Unable to resolve hostname '{host}'.")
    for ip in ip_list:
        if _is_ip_internal(ip):
            raise ValueError(f"Hostname '{host}' resolves to internal IP address {ip}.")

    return api_endpoint