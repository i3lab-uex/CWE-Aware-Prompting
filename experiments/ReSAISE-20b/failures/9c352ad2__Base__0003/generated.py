import re
import socket
from urllib.parse import urlparse

# Pre‑approved public API domains (example list)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "open.api.net",
}

# Regex to match private IP ranges (RFC1918, loopback, link‑local)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.|                         # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2\d|3[0-1])\.| # 172.16.0.0 – 172.31.255.255
        192\.168\.|                   # 192.168.0.0 – 192.168.255.255
        127\.|                        # loopback
        169\.254\.                    # link‑local
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or link‑local range."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all its IPv4 addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None, socket.AF_INET)]
    except socket.gaierror:
        # If the hostname cannot be resolved we treat it as unsafe
        return []

def _is_internal_ip(ip: str) -> bool:
    """Check if an IP address is internal or private."""
    return _is_private_ip(ip)

def process_webhook(webhook_url: str) -> str:
    """
    Validate that a webhook URL points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        URL provided by an external service.

    Returns
    -------
    str
        The validated URL if it points to a pre‑approved domain and is not an internal address.

    Raises
    ------
    ValueError
        If the domain is not approved or resolves to an internal IP address.
    """
    if not webhook_url:
        raise ValueError("Webhook URL must be a non‑empty string")

    parsed = urlparse(webhook_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against approved list (case‑insensitive)
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an approved endpoint")

    # Resolve hostname to IP addresses and ensure none are internal
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Unable to resolve hostname '{hostname}'")

    for ip in ips:
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{hostname}' is internal")

    # All checks passed – return the original URL
    return webhook_url