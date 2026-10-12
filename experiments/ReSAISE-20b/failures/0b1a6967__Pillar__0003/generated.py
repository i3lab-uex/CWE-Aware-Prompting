import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Regular expression for detecting localhost patterns
LOCALHOST_RE = re.compile(r'^(localhost|127\.0\.0\.1|::1)$', re.IGNORECASE)

# List of approved top‑level domains or domain patterns (example)
APPROVED_TLDS = (
    r'\.com$',
    r'\.org$',
    r'\.net$',
    r'\.io$',
    r'\.api$',
)

# Private IP ranges as defined by RFC 1918 and others
PRIVATE_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),   # link local
    ipaddress.ip_network('127.0.0.0/8'),      # loopback
    ipaddress.ip_network('::1/128'),          # IPv6 loopback
    ipaddress.ip_network('fe80::/10'),        # IPv6 link local
]

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    If host is not an IP literal, we conservatively return False
    (the caller should rely on DNS to resolve later).
    """
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP literal; skip private check
        return False

    for net in PRIVATE_RANGES:
        if ip in net:
            return True
    return False

def _is_approved_domain(host: str) -> bool:
    """
    Check that the hostname ends with one of the approved TLDs.
    This is a simple heuristic; real deployments may use
    a more sophisticated whitelist or certificate pinning.
    """
    host = host.lower()
    return any(re.search(tld, host) for tld in APPROVED_TLDS)

def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that the supplied URL points to an external, secure API endpoint.

    Parameters
    ----------
    endpoint_address : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The verified URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an insecure scheme, points to a private IP,
        or targets an unapproved domain.
    """
    if not isinstance(endpoint_address, str):
        raise ValueError('Endpoint address must be a string')

    parsed = urlparse(endpoint_address)

    # Scheme must be HTTPS
    if parsed.scheme.lower() != 'https':
        raise ValueError('Only HTTPS URLs are allowed')

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError('URL must contain a hostname')

    # Reject localhost patterns
    if LOCALHOST_RE.match(host):
        raise ValueError('Localhost addresses are disallowed')

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError('Private network addresses are disallowed')

    # Simple domain whitelist check
    if not _is_approved_domain(host):
        raise ValueError('Unapproved domain name')

    # Optionally enforce default port 443 if none is specified
    netloc = parsed.netloc
    if ':' not in netloc:
        netloc += ':443'
        parsed = parsed._replace(netloc=netloc)

    # Rebuild the URL to normalize it
    verified_url = urlunparse(parsed)
    return verified_url