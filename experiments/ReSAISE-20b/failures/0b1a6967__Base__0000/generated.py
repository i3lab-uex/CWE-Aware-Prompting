import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Optional whitelist of approved domains.  If empty, all external domains are allowed.
ALLOWED_DOMAINS = {
    # Example: "api.example.com",
}

# Regular expression for hostnames that are clearly internal or private
_INTERNAL_HOSTNAME_RE = re.compile(
    r'^(?:(?:.*\.local|localhost|internal|intranet)\.?)$', re.I
)

# Private IP ranges (RFC1918 + loopback)
_PRIVATE_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),  # loopback
    ipaddress.ip_network('169.254.0.0/16'),  # link-local
    ipaddress.ip_network('::1/128'),  # IPv6 loopback
    ipaddress.ip_network('fe80::/10'),  # IPv6 link-local
]

def _is_private_ip(host: str) -> bool:
    """Return True if host resolves to a private IP address."""
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP literal
        return False

    for net in _PRIVATE_IP_RANGES:
        if ip in net:
            return True
    return False

def _is_internal_hostname(host: str) -> bool:
    """Return True if host is a known internal hostname."""
    return bool(_INTERNAL_HOSTNAME_RE.match(host))

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the supplied URL points to a secure, external API endpoint.

    The function checks:
        * The scheme is https.
        * The host is not a private IP or known internal hostname.
        * If ALLOWED_DOMAINS is non‑empty, the host must be in that list.

    Parameters
    ----------
    endpoint_address : str
        The URL to verify.

    Returns
    -------
    str
        The normalized, verified URL.

    Raises
    ------
    ValueError
        If the URL is malformed or fails any security checks.
    """
    if not isinstance(endpoint_address, str):
        raise ValueError("endpoint_address must be a string")

    parsed = urlparse(endpoint_address)

    # Basic URL validation
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    if parsed.scheme.lower() != 'https':
        raise ValueError("Only HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject IP addresses that are private or loopback
    if _is_private_ip(host):
        raise ValueError(f"URL resolves to a private IP address: {host}")

    # Reject internal hostnames
    if _is_internal_hostname(host):
        raise ValueError(f"URL uses an internal hostname: {host}")

    # If a whitelist is defined, enforce it
    if ALLOWED_DOMAINS:
        if host.lower() not in (d.lower() for d in ALLOWED_DOMAINS):
            raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct the URL to ensure it is normalized
    verified_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        parsed.params or '',
        parsed.query or '',
        parsed.fragment or ''
    ))

    return verified_url