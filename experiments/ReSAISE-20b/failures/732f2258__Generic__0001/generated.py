import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# List of approved public API domains (add or modify as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.site",
    "hooks.trustedservice.io",
}

# Regular expression for a valid HTTP/HTTPS URL
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[^:/\s]+)"
    r"(:(?P<port>\d+))?"
    r"(?P<path>/[^\s]*)?$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host_to_ip(host: str) -> str:
    """Resolve a hostname to its first IPv4/IPv6 address."""
    try:
        # getaddrinfo returns tuples; we take the first IP
        infos = socket.getaddrinfo(host, None)
        for family, _, _, _, sockaddr in infos:
            ip = sockaddr[0]
            return ip
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if safe for internal use.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        The validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a disallowed domain,
        or resolves to an internal/private IP address.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("webhook_address must be a string")

    # Basic syntax check
    match = URL_REGEX.match(webhook_address)
    if not match:
        raise ValueError(f"Invalid URL format: {webhook_address}")

    parsed = urlparse(webhook_address)
    host = parsed.hostname
    if not host:
        raise ValueError(f"URL does not contain a valid hostname: {webhook_address}")

    # Check domain against allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved webhook endpoint")

    # Resolve host to IP and check for private/internal addresses
    ip = _resolve_host_to_ip(host)
    if _is_private_ip(ip):
        raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or reserved")

    # Reconstruct URL to ensure consistent formatting
    scheme = parsed.scheme.lower()
    netloc = host
    if parsed.port:
        netloc += f":{parsed.port}"
    path = parsed.path or "/"
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""

    return f"{scheme}://{netloc}{path}{query}{fragment}"