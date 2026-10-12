import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# List of approved API hostnames (case‑insensitive)
APPROVED_HOSTS = {
    "api.mycompany.com",
    "service.example.org",
}

# Regular expression to detect private or loopback IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.         # 10.0.0.0 – 10.255.255.255
        | 172\.(?:1[6-9]|2\d|3[0-1])\.   # 172.16.0.0 – 172.31.255.255
        | 192\.168\.   # 192.168.0.0 – 192.168.255.255
        | 127\.0\.0\.1 # loopback
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(hostname: str) -> bool:
    """
    Resolve the hostname to an IP address and determine if it is a private
    or loopback address.  If resolution fails, treat it as non‑private.
    """
    try:
        ip = socket.gethostbyname(hostname)
        # Quick regex check for common private ranges
        if PRIVATE_IP_REGEX.match(ip):
            return True
        # Use ipaddress module for a definitive check
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
            ip
        ).is_loopback
    except Exception:
        # If we cannot resolve the host, treat it as non‑private to avoid
        # unintentionally blocking valid external domains.
        return False


def _is_approved_host(hostname: str) -> bool:
    """
    Check whether the hostname is in the approved list.  The comparison
    is case‑insensitive.
    """
    return hostname.lower() in APPROVED_HOSTS


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and return it if it references an approved
    API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL supplied by an external service that should trigger a
        call to our internal API.

    Returns
    -------
    str
        The original URL if it is valid and approved.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, points to a private/internal
        IP address, or its hostname is not in the approved list.
    """
    if not isinstance(url_hook, str):
        raise ValueError("url_hook must be a string")

    parsed: ParseResult = urlparse(url_hook)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Reject private or loopback IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private or loopback address")

    # Host must be in the approved list
    if not _is_approved_host(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not approved")

    # All checks passed; return the original URL
    return url_hook