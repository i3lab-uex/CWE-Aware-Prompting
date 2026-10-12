import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.company.org",
    "gateway.otherservice.net"
}

# Regular expression to detect private or reserved IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:  # start of the whole IP
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |                # 10.0.0.0 – 10.255.255.255
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) | # 172.16.0.0 – 172.31.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3}) |                  # 192.168.0.0 – 192.168.255.255
        (?:169\.254\.\d{1,3}\.\d{1,3}) |                  # Link-local
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3}) |              # Loopback
        (?:0\.\d{1,3}\.\d{1,3}\.\d{1,3}) |                # 0.0.0.0
        (?:255\.255\.255\.255)                            # Broadcast
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If not a valid IP address, treat as non-private
        return False

def _is_private_hostname(hostname: str) -> bool:
    """Return True if the hostname resolves to a private IP."""
    try:
        # Resolve all addresses for the hostname
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If hostname cannot be resolved, treat as unsafe
        return True

    for info in infos:
        addr = info[4][0]
        if _is_private_ip(addr):
            return True
    return False

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal use.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and normalized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in ALLOWED_DOMAINS or if the URL points to an internal/private network.
    """
    parsed = urlparse(webhook_address)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Normalise the hostname (lowercase, strip trailing dot)
    hostname = parsed.hostname.lower().rstrip('.')
    if not hostname:
        raise ValueError("Invalid URL: empty hostname")

    # Check against allowed domains
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an approved API endpoint")

    # Check for private IPs or hostnames that resolve to private addresses
    if _is_private_hostname(hostname):
        raise ValueError("URL points to a private or internal network")

    # Rebuild the URL with normalized components
    safe_parts = (
        parsed.scheme,
        hostname,
        parsed.port if parsed.port else '',
        parsed.path or '/',
        parsed.params,
        parsed.query,
        ''  # fragment is omitted for internal calls
    )
    safe_url = urlunparse(safe_parts)

    return safe_url