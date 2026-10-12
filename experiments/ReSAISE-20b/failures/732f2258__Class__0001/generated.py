import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Whitelisted public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    'api.example.com',
    'services.allowed.org',
    'public.api.net'
}

# Regex to quickly reject obvious non‑URL inputs
_URL_RE = re.compile(
    r'^(?:(?:http|https)://)'
    r'(?:[^\s:@/]+(?::[^\s@]*)?@)?'          # optional user:pass@
    r'(?P<host>[^:/\s]+)'                    # host
    r'(?:\:\d+)?'                            # optional port
    r'(?:[/?#][^\s]*)?$', re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback,
    or link‑local range.
    """
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address (e.g., hostname that cannot be resolved)
        return False

def _resolve_host(host: str) -> list[str]:
    """
    Resolve the host to all IPv4 addresses.  If resolution fails,
    return an empty list.
    """
    try:
        # getaddrinfo may return IPv6 addresses; filter for IPv4 only
        infos = socket.getaddrinfo(host, None, family=socket.AF_INET)
        return [sock[4][0] for sock in infos]
    except socket.gaierror:
        return []

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal use.

    Parameters
    ----------
    webhook_address : str
        URL supplied by an external service.

    Returns
    -------
    str
        The validated, original URL.

    Raises
    ------
    ValueError
        If the URL is malformed, its domain is not in the whitelist,
        or it resolves to a private/internal IP.
    """
    # Basic URL format check
    match = _URL_RE.match(webhook_address)
    if not match:
        raise ValueError("Malformed URL")

    parsed = urlparse(webhook_address)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in ('http', 'https'):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalise host to lower case
    host = parsed.hostname.lower()
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Resolve host and check for private IPs
    ips = _resolve_host(host)
    if not ips:
        # If we cannot resolve, treat as unsafe
        raise ValueError(f"Could not resolve host: {host}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Host {host} resolves to private IP: {ip}")

    # Reconstruct the URL (in case of parsing differences)
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return safe_url