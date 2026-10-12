import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.partner.com",
    "services.thirdparty.io",
}

# Regex to detect private IP address patterns
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|127\.|192\.168\.|169\.254\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not an IP address; assume it's a hostname.
        return False

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a safe internal API URL.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A validated and normalized URL suitable for internal use.

    Raises
    ------
    ValueError
        If the domain is not in ALLOWED_DOMAINS or points to a private network.
    """
    if not webhook_endpoint:
        raise ValueError("Empty URL provided")

    parsed = urlparse(webhook_endpoint)

    # Ensure scheme is present and safe
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve host to IP if possible and check for private ranges
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # If the hostname is an IP address, validate directly
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if _is_private_ip(host):
            raise ValueError(f"URL points to a private IP address: {host}")
    else:
        # If hostname is not an IP, check against allowed domains
        if host.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{host}' is not an allowed webhook endpoint")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragment should be removed for internal requests
    ))

    return safe_url