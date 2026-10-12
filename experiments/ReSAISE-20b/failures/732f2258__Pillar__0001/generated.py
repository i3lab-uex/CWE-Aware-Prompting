import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define the set of approved public API domains
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.external.org",
    "public-api.company.net"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.|                # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])\.|  # 172.16.0.0/12
        192\.168\.|          # 192.168.0.0/16
        127\.|               # Loopback
        ::1$                 # IPv6 loopback
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host string is a private IP address.
    Handles both IPv4 and IPv6.
    """
    try:
        # Try parsing as IP address
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; check regex for IPv4 patterns
        return bool(PRIVATE_IP_REGEX.match(host))

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal API usage.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated, normalized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list or points to a private/internal network.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("Webhook address must be a string")

    parsed = urlparse(webhook_address)

    # Ensure scheme is present and secure
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Extract hostname (handles IPv6 with brackets)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal IP address")

    # Reject domains not in the allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct a normalized URL (remove userinfo, default ports)
    netloc = host
    if parsed.port:
        # Only include port if it's non-standard for the scheme
        default_port = 443 if parsed.scheme == "https" else 80
        if parsed.port != default_port:
            netloc = f"{host}:{parsed.port}"
    normalized_url = urlunparse(
        (parsed.scheme, netloc, parsed.path or "/", "", parsed.query, "")
    )
    return normalized_url