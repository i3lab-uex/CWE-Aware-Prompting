import re
import socket
from urllib.parse import urlparse

# Whitelisted public API domains (example list)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public-api.myservice.org",
    "data-provider.net",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to its IPv4 addresses."""
    try:
        # getaddrinfo may return both IPv4 and IPv6; we filter for IPv4
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
        return [info[4][0] for info in infos]
    except socket.gaierror:
        # Hostname could not be resolved
        return []

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL against a whitelist of public API endpoints
    and ensure it does not target internal/private network addresses.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized and validated URL that is safe for internal API calls.

    Raises
    ------
    ValueError
        If the domain is not whitelisted or resolves to a private IP address.
    """
    if not webhook_endpoint:
        raise ValueError("webhook_endpoint must be a non-empty string")

    parsed = urlparse(webhook_endpoint)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain against whitelist
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Case-insensitive comparison
    if hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Resolve hostname to IPs and check for private addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for domain '{hostname}' is private")

    # Reconstruct the URL to ensure it has no query fragments that might be abused
    sanitized_url = f"{parsed.scheme}://{hostname}"
    if parsed.port:
        sanitized_url += f":{parsed.port}"

    return sanitized_url