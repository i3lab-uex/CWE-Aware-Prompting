import re
from urllib.parse import urlparse, urlunparse
import ipaddress
import socket

# Whitelist of approved public API domains (case‑insensitive)
WHITELIST_DOMAINS = {
    "api.example.com",
    "public.api.service.org",
    "hooks.myapp.io",
}

# Regex for detecting private IP ranges (IPv4 & IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.|127\.|169\.254\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\."
    r"|::1$|fc00:|fe80:)",
    re.IGNORECASE,
)


def _is_private_ip(hostname: str) -> bool:
    """
    Determine whether the given hostname resolves to a private IP address.
    """
    try:
        # Resolve all addresses for the hostname
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If resolution fails treat as non‑private to avoid blocking
        return False

    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback:
                return True
        except ValueError:
            # Invalid IP address, skip
            continue
    return False


def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API endpoints.
    
    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized and validated URL that can be safely used for internal API calls.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist or if it resolves to a private/internal address.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against whitelist (case‑insensitive)
    if hostname.lower() not in WHITELIST_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

    # Prevent private IP access
    if PRIVATE_IP_REGEX.match(hostname) or _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or internal network address")

    # Reconstruct the URL ensuring no userinfo, fragments, etc.
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query parameters
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url