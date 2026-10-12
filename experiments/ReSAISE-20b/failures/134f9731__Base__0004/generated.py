import re
from urllib.parse import urlparse, urlunparse
import socket

# Whitelist of allowed public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public.api.service.org",
    "data.provider.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # 172.16.0.0 – 172.31.255.255
        172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|
        # 192.168.0.0 – 192.168.255.255
        192\.168\.\d{1,3}\.\d{1,3}|
        # Loopback
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # Link-local
        169\.254\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return bool(PRIVATE_IP_REGEX.match(ip))


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all IPv4 addresses."""
    try:
        infos = socket.getaddrinfo(host, None, family=socket.AF_INET)
    except socket.gaierror:
        return []

    ips = {info[4][0] for info in infos}
    return list(ips)


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it is used for internal API calls.

    Parameters
    ----------
    webhook_endpoint : str
        The URL supplied by an external source.

    Returns
    -------
    str
        A sanitized and validated URL that can be safely used internally.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, the domain is not whitelisted,
        or it resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed = urlparse(webhook_endpoint)

    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for webhooks.")

    # Extract hostname
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid URL: missing hostname.")

    # Check against whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist.")

    # Resolve hostname to IPs and ensure none are private
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Unable to resolve hostname '{host}'.")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for host '{host}' is in a private range."
            )

    # Reconstruct the URL to ensure no query params or fragments are present
    safe_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "/", "", "", "")
    )
    return safe_url