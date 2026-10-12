import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "public-api.myservice.org",
    "services.thirdparty.io",
}

# Regular expression to detect IP addresses in the netloc
_IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP string is a private, loopback or link‑local address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _hostname_to_ip(hostname: str) -> str | None:
    """
    Resolve a hostname to its first IPv4 address.
    If resolution fails, return None.  This helper is used only for safety checks
    and does NOT perform any network operation that could be abused by an attacker.
    """
    try:
        # Use getaddrinfo to support IPv4 and IPv6; pick the first IPv4 address
        for family, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
            if family == socket.AF_INET:
                return sockaddr[0]
    except Exception:
        pass
    return None

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL string supplied by the external service.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that can safely be used for internal API calls.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list, or if it resolves to a private
       /internal network address.
    """
    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and host")

    # Normalize the hostname to lowercase
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # 1. Check against the whitelist
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an approved API endpoint")

    # 2. Detect if the host part is an IP address
    if _IP_RE.match(hostname):
        if _is_private_ip(hostname):
            raise ValueError(f"IP address '{hostname}' is private or internal")
    else:
        # 3. Resolve the hostname to an IP and ensure it is not private
        resolved_ip = _hostname_to_ip(hostname)
        if resolved_ip and _is_private_ip(resolved_ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address")

    # Reconstruct the URL using only the parsed components
    sanitized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=hostname if not parsed.port else f"{hostname}:{parsed.port}",
    ).geturl()

    return sanitized