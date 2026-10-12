import re
import socket
from urllib.parse import urlparse, urlunparse

# Allowed public API domains (example list)
ALLOWED_DOMAINS = {
    "api.example.com",
    "hooks.partner.net",
    "webhook.service.org",
}

# Regular expression for private IP ranges (RFC1918 & loopback)
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(                               # start of string
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # 10.0.0.0/8 or 127.0.0.0/8
        (172\.(1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        (192\.168)\.\d{1,3}\.\d{1,3} |                 # 192.168.0.0/16
        ::1                                            # IPv6 loopback
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    # Handle IPv6 literal in brackets
    ip = ip.strip("[]")
    try:
        packed_ip = socket.inet_pton(socket.AF_INET, ip)
    except OSError:
        try:
            packed_ip = socket.inet_pton(socket.AF_INET6, ip)
        except OSError:
            # Not a valid IP address
            return False

    if _PRIVATE_IP_RE.match(ip):
        return True

    # For IPv6, check global unicast
    if packed_ip[0] & 0xFE == 0xFC:  # fc00::/7
        return True

    return False


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before using it internally.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in ALLOWED_DOMAINS or if the URL resolves to a private IP.
    """
    parsed = urlparse(webhook_endpoint)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname (may be an IP or a domain)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve to IP(s) and ensure none are private
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host {host}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to a private IP: {ip}")

    # Domain whitelist check (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {host} is not allowed")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url