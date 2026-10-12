import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames or subdomains (case‑insensitive)
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.company.com",
}

# Private IP networks that must be blocked
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),          # loopback
    ipaddress.ip_network("169.254.0.0/16"),       # link‑local
    ipaddress.ip_network("::1/128"),             # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),            # Unique local address (ULA)
]

# Regex to detect obvious local hostnames
LOCAL_HOSTNAME_RE = re.compile(r"^(localhost|127\.0\.0\.1)$", re.IGNORECASE)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is in a private or local network."""
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    for net in PRIVATE_NETWORKS:
        if ip_obj in net:
            return True
    return False


def _is_approved_host(host: str) -> bool:
    """Check if the host is in the approved list."""
    return host.lower() in APPROVED_HOSTS


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service.

    Returns
    -------
    str
        A safely validated URL referencing an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it targets an internal network location.
    """
    if not webhook_link:
        raise ValueError("Empty URL provided")

    parsed = urlparse(webhook_link)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Disallow empty netloc (e.g., "http:///path")
    if not parsed.netloc:
        raise ValueError("URL missing host component")

    # Check for obvious local hostnames
    if LOCAL_HOSTNAME_RE.match(parsed.netloc.split(":")[0]):
        raise ValueError("URL resolves to a local host")

    # Resolve potential IP address in the hostname
    host = parsed.netloc.split(":")[0]  # strip port if present

    try:
        ip_obj = ipaddress.ip_address(host)
        # If host is an IP address, ensure it's not private
        if _is_private_ip(host):
            raise ValueError("URL resolves to a private IP address")
    except ValueError:
        # Not an IP literal; treat as hostname
        if not _is_approved_host(host):
            raise ValueError(f"Host '{host}' is not in the list of approved endpoints")

    # Reconstruct URL to ensure consistent formatting
    sanitized_url = urlunparse(parsed._replace(fragment=""))  # drop fragment for safety

    return sanitized_url