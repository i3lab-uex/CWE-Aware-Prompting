import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames (may include subdomains or wildcard patterns)
APPROVED_HOST_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\.internal\.company$",
]

# Regular expression to detect IPv4 or IPv6 addresses
IP_REGEX = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$|^\[?[a-fA-F0-9:]+(?:\]|$)")


def _is_approved_host(host: str) -> bool:
    """Check if the host matches one of the approved patterns."""
    for pattern in APPROVED_HOST_PATTERNS:
        if re.match(pattern, host):
            return True
    return False


def _is_internal_ip(host: str) -> bool:
    """Return True if host is a private or loopback IP address."""
    # If host looks like an IP address, validate it
    if IP_REGEX.match(host):
        try:
            ip_obj = ipaddress.ip_address(host)
            return ip_obj.is_private or ip_obj.is_loopback
        except ValueError:
            # Not a valid IP address; treat as external
            return False

    # If host is a hostname, we cannot reliably resolve it without network access.
    # For safety, assume it's external unless explicitly in approved patterns.
    return False


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to reference an approved endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to an internal network location.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract host and strip port if present
    netloc = parsed.netloc.split(":")[0]

    # Reject internal IP addresses or loopback
    if _is_internal_ip(netloc):
        raise ValueError("URL points to an internal IP address")

    # Reject if host is not in the approved list
    if not _is_approved_host(netloc):
        raise ValueError(f"Host '{netloc}' is not an approved API endpoint")

    # Reconstruct the URL to ensure it has no fragments or query parameters that might be malicious
    sanitized = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized