import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.api.org",
    "webhook.provider.net",
}

# Regex to detect private IP addresses (IPv4 and IPv6)
_PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.) |          # IPv4
    (^::1$|^fe80:|^fc00:|^fd00:)                                       # IPv6
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Check if a host is a private IP address or an IPv6 private block.
    Returns True if the host resolves to a private network.
    """
    try:
        # Resolve hostname to IP(s) if it's an address
        ip_obj = ipaddress.ip_address(host)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        # Not an IP address; check regex for known private prefixes
        return bool(_PRIVATE_IP_REGEX.search(host))


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it for internal API usage.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and safe URL that can be used internally.

    Raises
    ------
    ValueError
        If the domain is not in ALLOWED_DOMAINS or if the URL points to a private/internal network.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("webhook_address must be a string")

    parsed = urlparse(webhook_address)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Extract host and port
    host = parsed.hostname
    if not host:
        raise ValueError("Could not parse hostname from URL")

    # Reject private or loopback IPs
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private or loopback IP: {host}")

    # Reject domains not in the allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragment stripped
    ))

    return safe_url