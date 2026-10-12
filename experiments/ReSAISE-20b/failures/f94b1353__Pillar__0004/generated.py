import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API endpoints (domains only)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.mycorp.org",
    "public.api.company.net",
}

# Regular expression to detect common private IP address patterns
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|
    ^169\.254\.)
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or reserved address."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address; treat as non-private
        return False

def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return domain.lower() in APPROVED_DOMAINS

def manage_webhook(url_hook: str) -> str:
    """
    Validate and return a safe URL that references an approved public API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, points to a private or internal
        network address, or does not belong to an approved domain.
    """
    if not isinstance(url_hook, str):
        raise ValueError("url_hook must be a string")

    # Parse the URL
    parsed = urlparse(url_hook)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Split host and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses or localhost
    if PRIVATE_IP_REGEX.search(host) or _is_private_ip(host):
        raise ValueError(f"URL points to a private network address: {host}")

    # Reject unapproved domains
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure it contains only the components we want
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query string if any
        ""   # fragment
    ))

    return safe_url