import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# Regular expression to detect localhost or 127.0.0.1 hostnames
LOCALHOST_RE = re.compile(r'^(localhost|127\.0\.0\.1)$', re.IGNORECASE)

# Private IP ranges as defined by RFC1918 and loopback
PRIVATE_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),          # loopback
    ipaddress.ip_network('169.254.0.0/16'),       # link-local
    ipaddress.ip_network('::1/128'),             # IPv6 loopback
    ipaddress.ip_network('fc00::/7'),            # Unique local address (ULA)
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string belongs to a private or link‑local range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that a URL points to an external, non‑internal API endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL to be verified.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain, a private IP address,
        localhost, or uses an unsafe scheme.
    """
    # Basic parsing
    parsed: ParseResult = urlparse(api_endpoint)

    if not parsed.scheme or parsed.scheme.lower() not in ('http', 'https'):
        raise ValueError(f"URL must use http or https scheme: {api_endpoint}")

    # Reject URLs with userinfo (username/password) for security reasons
    if parsed.username or parsed.password:
        raise ValueError(f"URL must not contain userinfo: {api_endpoint}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"URL must contain a valid hostname: {api_endpoint}")

    # Reject localhost or 127.0.0.1 hostnames
    if LOCALHOST_RE.match(hostname):
        raise ValueError(f"Localhost URLs are disallowed: {api_endpoint}")

    # If hostname is an IP address, check for private ranges
    try:
        ipaddress.ip_address(hostname)
        if _is_private_ip(hostname):
            raise ValueError(f"Private IP addresses are disallowed: {api_endpoint}")
    except ValueError:
        # hostname is not an IP address; proceed to next checks
        pass

    # Additional optional check: ensure hostname is a valid DNS name
    if not re.match(r'^[A-Za-z0-9.-]+$', hostname):
        raise ValueError(f"Hostname contains invalid characters: {api_endpoint}")

    # All checks passed; return the original URL
    return api_endpoint