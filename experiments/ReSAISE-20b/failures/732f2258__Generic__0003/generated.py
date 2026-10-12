import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.public.net",
    "gateway.api.org",
}

# Regular expression to detect private or loopback IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.)|                                   # Loopback
    (^10\.)|                                     # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\. )|              # Class B private
    (^192\.168\.)|                               # Class C private
    (^169\.254\.)                                 # Link‑local
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if a host string is an IP address that belongs to a private or
    loopback network.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, treat as non‑private for this check
        return False

def _validate_domain(host: str) -> None:
    """
    Validate that the hostname belongs to an approved domain list and is not a
    private IP or internal address.
    """
    host_lower = host.lower()

    # Reject explicit IP addresses that are private or loopback
    if re.match(PRIVATE_IP_REGEX, host_lower):
        raise ValueError(f"URL points to a private IP address: {host}")

    if _is_private_ip(host_lower):
        raise ValueError(f"URL points to a private IP address: {host}")

    # If host is an IP, it's not in the allowed domain list
    try:
        ipaddress.ip_address(host_lower)
        # IP address found, but not allowed
        raise ValueError(f"IP addresses are not permitted: {host}")
    except ValueError:
        # Not an IP, proceed to domain check
        pass

    if host_lower not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the allowed list")

def analyze_webhook(webhook_address: str) -> str:
    """
    Parse and validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_address : str
        The raw URL string from the external service.

    Returns
    -------
    str
        A sanitized and validated URL that can be safely used for internal API
        requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it points to a
        private/internal network.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("webhook_address must be a string")

    parsed = urlparse(webhook_address)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    _validate_domain(parsed.hostname)

    # Reconstruct the URL to guarantee normalisation
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or "",
    ))
    return sanitized