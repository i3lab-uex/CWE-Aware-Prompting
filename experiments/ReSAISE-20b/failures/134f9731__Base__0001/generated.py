import re
import socket
from urllib.parse import urlparse, urlunparse

# Allowed public API domains (add or modify as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.publicapi.org",
}

# Regular expression for private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if IP is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str) -> set[str]:
    """
    Resolve a hostname to all its IPv4 addresses.
    Returns a set of IP strings.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror:
        return set()
    return {info[4][0] for info in infos}

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate that the provided webhook endpoint is safe to call internally.

    Parameters
    ----------
    webhook_endpoint : str
        External webhook URL supplied by an upstream component.

    Returns
    -------
    str
        The same URL if it is safe to call internally.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist or resolves to a private IP.
    """
    if not webhook_endpoint:
        raise ValueError("Webhook endpoint must be a non-empty string")

    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Normalize domain to lowercase for comparison
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("Invalid URL: unable to extract hostname")

    # Check against whitelist
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the allowed list")

    # Resolve hostname and ensure no private IPs are returned
    resolved_ips = _resolve_hostname(hostname)
    if not resolved_ips:
        raise ValueError(f"Hostname '{hostname}' could not be resolved")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' is a private address")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return safe_url