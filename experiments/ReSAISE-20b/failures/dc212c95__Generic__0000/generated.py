import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.org",
    "hooks.partner.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),  # Unique local addresses
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in net for net in PRIVATE_IP_RANGES)
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        return [
            result[4][0]
            for result in socket.getaddrinfo(hostname, None)
        ]
    except socket.gaierror:
        return []

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a safe internal URL.

    Parameters
    ----------
    webhook_endpoint : str
        The full URL supplied by an external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be used for internal API requests.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, has a disallowed domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    # Only http or https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize hostname (case-insensitive)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Domain must be in the allowed list
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the allowed list")

    # Resolve hostname to IPs and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP: {ip}")

    # Reconstruct the URL ensuring no userinfo or port that might be unsafe
    safe_netloc = hostname
    if parsed.port:
        safe_netloc += f":{parsed.port}"

    safe_url = urlunparse(
        (
            parsed.scheme,
            safe_netloc,
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query string
            ""   # fragment
        )
    )

    return safe_url