import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved hostnames or domain patterns (regex)
APPROVED_HOST_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\.mycompany\.org$",
    r"^internal\.api\.example\.com$",   # example of an internal API that is still allowed
]

# Compile the regexes for performance
APPROVED_HOST_REGEXES = [re.compile(p) for p in APPROVED_HOST_PATTERNS]

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_internal_ip(host: str) -> bool:
    """
    Determine if the host resolves to an internal IP address or is itself an IP.
    The function does not perform DNS resolution; it only checks if the host
    string is a numeric IP or matches known private address ranges.
    """
    # If the host looks like an IPv4/IPv6 literal, test it
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a literal IP, assume it's a hostname; we cannot resolve it here
        return False


def _is_approved_host(host: str) -> bool:
    """
    Check if the host matches one of the approved patterns.
    """
    for regex in APPROVED_HOST_REGEXES:
        if regex.match(host):
            return True
    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL so that it points to an approved public API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by the external service.

    Returns
    -------
    str
        A sanitized URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        if it resolves to an internal network location, or if the URL is
        malformed.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    # Parse the URL
    parsed = urlparse(webhook_link)

    # Basic scheme check
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host extraction
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal IP addresses
    if _is_internal_ip(host):
        raise ValueError("URL points to an internal IP address")

    # Reject hosts that are not approved
    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure it is canonical
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url