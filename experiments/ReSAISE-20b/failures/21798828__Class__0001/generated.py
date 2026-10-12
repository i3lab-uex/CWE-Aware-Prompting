import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# List of approved API hostnames (exact matches or with wildcard subdomains)
APPROVED_HOSTNAMES = [
    "api.mycompany.com",
    "*.internal.mycompany.com",  # wildcard support
]

# Regex to detect private IP ranges and loopback addresses
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not an IP address (likely a hostname)
        return False

def _is_approved_host(host: str) -> bool:
    """Check if host matches an approved hostname or wildcard."""
    for pattern in APPROVED_HOSTNAMES:
        if pattern.startswith("*."):
            # Wildcard subdomain
            suffix = pattern[2:]
            if host.endswith(suffix) and host.count(".") >= suffix.count("."):
                return True
        else:
            if host == pattern:
                return True
    return False

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return a safe, approved internal API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or points to a private IP.
    """
    if not webhook_link:
        raise ValueError("Webhook link cannot be empty")

    parsed = urlparse(webhook_link)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with an empty netloc (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Reject URLs that attempt to use port numbers outside the approved list
    if parsed.port and not (1 <= parsed.port <= 65535):
        raise ValueError(f"Invalid port number: {parsed.port}")

    # Detect if the host is a private IP
    host = parsed.hostname.lower()
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Validate hostname against approved list
    if not _is_approved_host(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure no hidden components
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
        path=parsed.path or "/",
        params="",
        query="",
        fragment=""
    )
    return urlunparse(sanitized)