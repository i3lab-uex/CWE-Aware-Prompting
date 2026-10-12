import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# Configuration: allowed public API domains (case‑insensitive)
# ------------------------------------------------------------------
ALLOWED_DOMAINS = {
    'api.example.com',
    'service.internal.com',   # replace with your real domains
}

# ------------------------------------------------------------------
# Helper: check if an IP address is private or reserved
# ------------------------------------------------------------------
def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is in a private or reserved address block."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        )
    except ValueError:
        # Not a valid IP address
        return True

# ------------------------------------------------------------------
# Main validation function
# ------------------------------------------------------------------
def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL received from the external service.

    Returns
    -------
    str
        A fully validated and normalised URL that can safely be used for
        internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a disallowed domain,
        or resolves to a private/internal IP address.
    """
    # Parse the URL and normalise scheme
    parsed = urlparse(webhook_endpoint.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Normalise scheme to https for security
    scheme = parsed.scheme.lower()
    if scheme not in {'http', 'https'}:
        raise ValueError("Only http/https schemes are allowed")

    # Ensure host is not an IP address that we don't want
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against the allowed list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of allowed endpoints")

    # Resolve hostname to IP addresses (IPv4/IPv6)
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from None

    # Validate each resolved IP
    for family, _, _, _, sockaddr in addrinfo:
        ip_str = sockaddr[0]
        if _is_private_ip(ip_str):
            raise ValueError(f"Resolved IP '{ip_str}' for host '{host}' is private or reserved")

    # Reconstruct a normalised URL (drop userinfo, fragment)
    netloc = parsed.hostname
    if parsed.port:
        netloc += f":{parsed.port}"
    normalised = urlunparse((scheme, netloc, parsed.path or '/', '', '', ''))

    return normalised