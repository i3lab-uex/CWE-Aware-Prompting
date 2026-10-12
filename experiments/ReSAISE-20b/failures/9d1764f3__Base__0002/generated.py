import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Whitelisted public API domains (add as needed)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "service.otherdomain.org",
    "public.api.net"
}

# Regex to validate basic URL format
URL_REGEX = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?P<host>[^/:?#]+)'
    r'(?:\:(?P<port>\d+))?'
    r'(?P<path>/[^?#]*)?'
    r'(?:\?(?P<query>[^#]*))?'
    r'(?:#(?P<fragment>.*))?$',
    re.IGNORECASE
)


def _is_private_ip(ip: str) -> bool:
    """Return True if IP is private, loopback or link-local."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all its IP addresses."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal use.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used internally.

    Raises
    ------
    ValueError
        If the URL is malformed, its domain is not whitelisted,
        or it resolves to a private/internal IP address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    match = URL_REGEX.match(webhook_link)
    if not match:
        raise ValueError(f"Invalid URL format: {webhook_link}")

    scheme = match.group("scheme")
    host = match.group("host").lower()
    port = match.group("port") or ("443" if scheme == "https" else "80")
    path = match.group("path") or ""
    query = match.group("query")
    fragment = match.group("fragment")

    # Check domain against whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Resolve host and ensure no private IPs
    ips = _resolve_host(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private/internal")

    # Reconstruct a canonical URL (no fragment)
    safe_url = urlunparse((scheme, f"{host}:{port}", path, "", query or "", ""))

    return safe_url