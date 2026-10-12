import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (hostnames or CIDR blocks)
WHITELIST = {
    "api.example.com",
    "service.otherdomain.org",
    "172.20.0.0/16",   # Example public CIDR block
}

# Regular expression to detect private IP ranges (RFC1918)
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.0\.0\.1$)|                                   # Loopback
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$)|                  # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$)|      # Class B private
    (^192\.168\.\d{1,3}\.\d{1,3}$)                       # Class C private
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False

def _is_whitelisted(host: str) -> bool:
    """Check if the host is in the whitelist or matches a CIDR block."""
    # Direct match
    if host.lower() in WHITELIST:
        return True

    # CIDR block match
    for cidr in WHITELIST:
        if '/' in cidr:  # CIDR notation
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                if ipaddress.ip_address(host) in network:
                    return True
            except ValueError:
                continue  # skip invalid entries

    return False

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal API calls.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A validated and sanitized URL that can be used internally.

    Raises
    ------
    ValueError
        If the URL's domain is not from the approved API endpoint list or if it points to an internal/private address.
    """
    # Basic parsing
    parsed = urlparse(callback_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Reject non-HTTP(S) schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Check for private IP addresses or loopback
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private or loopback IP address")

    # Check against whitelist
    if not _is_whitelisted(host):
        raise ValueError(f"Host '{host}' is not in the whitelist")

    # Reconstruct a safe URL preserving path, query, and fragment
    safe_url = urlunparse(parsed._replace(scheme="https", netloc=host))
    return safe_url