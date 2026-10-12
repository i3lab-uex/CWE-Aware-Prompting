import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of approved API hostnames (can include subdomains)
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.company.com",
}

# Regular expression to match private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private address."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False

def _is_approved_host(host: str) -> bool:
    """Check if the host is in the approved list or a subdomain."""
    # Normalize to lowercase
    host = host.lower()
    if host in APPROVED_HOSTS:
        return True
    # Allow subdomains of approved hosts
    for approved in APPROVED_HOSTS:
        if host.endswith("." + approved):
            return True
    return False

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A safely validated, normalized URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the approved list or targets a private/internal network.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    # Parse the URL
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Reject URLs that are not HTTP/HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Resolve percent-encoding in hostname
    host = unquote(parsed.hostname or "")
    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not approved")

    # Check for private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private IP address")

    # Optional: Reject URLs pointing to localhost or 127.0.0.1
    if host in {"localhost", "127.0.0.1"}:
        raise ValueError("URL points to localhost, which is disallowed")

    # Reconstruct a clean URL (preserve path, query, fragment)
    safe_url = parsed._replace(netloc=parsed.netloc).geturl()

    return safe_url