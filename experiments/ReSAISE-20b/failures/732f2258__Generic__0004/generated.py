import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "api.publicservice.net"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)   # IPv4 private
    |(^fc00:|^fd00:)                                         # IPv6 unique local
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Check if the given host is a private IP address."""
    try:
        # Handle IPv6 literals in brackets
        if host.startswith("[") and host.endswith("]"):
            host = host[1:-1]
        # Attempt to parse as IP
        ipaddress.ip_address(host)
        return host in (
            "127.0.0.1",
            "localhost",
            *ipaddress.ip_network("10.0.0.0/8").hosts(),
            *ipaddress.ip_network("172.16.0.0/12").hosts(),
            *ipaddress.ip_network("192.168.0.0/16").hosts(),
        )
    except ValueError:
        # Not an IP, check regex for private patterns
        return bool(PRIVATE_IP_REGEX.search(host))

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal API use.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and normalized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in ALLOWED_DOMAINS or if the URL points to a private/internal network.
    """
    parsed = urlparse(webhook_address)

    # Ensure scheme is present
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https).")

    # Validate scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed.")

    # Extract hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")

    # Reject private IPs or internal domains
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal network.")

    # Normalize domain: lowercase and strip 'www.'
    normalized_host = host.lower()
    if normalized_host.startswith("www."):
        normalized_host = normalized_host[4:]

    # Check against allowed domains
    if normalized_host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{normalized_host}' is not authorized.")

    # Reconstruct the URL with normalized host
    safe_parsed = parsed._replace(netloc=f"{normalized_host}:{parsed.port or ''}".rstrip(":"))
    safe_url = urlunparse(safe_parsed)

    return safe_url