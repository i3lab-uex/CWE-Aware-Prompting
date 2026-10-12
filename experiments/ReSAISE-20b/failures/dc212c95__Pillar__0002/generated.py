import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (example entries)
ALLOWED_DOMAINS = {
    "api.example.com",
    "hooks.service.org",
    "webhook.partner.net",
}

# Regular expression to validate the overall URL structure
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[^\s:/?#]+)"
    r"(:(?P<port>\d+))?"
    r"(?P<path>/[^\s?#]*)?"
    r"(\?(?P<query>[^\s#]*))?"
    r"(#[\w-]*)?$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if an IP address is private, loopback or reserved.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    Returns an empty list if resolution fails.
    """
    try:
        return [info[4][0] for info in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL string to validate.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for internal API calls.

    Raises
    ------
    ValueError
        If the URL does not use HTTPS, points to a disallowed domain,
        or resolves to an internal/private IP address.
    """
    # Basic structural validation
    match = URL_REGEX.match(webhook_endpoint)
    if not match:
        raise ValueError("Malformed URL")

    components = match.groupdict()
    scheme = components["scheme"].lower()
    host = components["host"]
    port = components.get("port")
    path = components.get("path") or "/"
    query = components.get("query")

    if scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Ensure the host is in the approved list (case-insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved webhook endpoint")

    # Resolve the host to IP addresses and check for private networks
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Unable to resolve host: {host}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP address: {ip}")

    # Reconstruct a normalized URL
    netloc = f"{host}:{port}" if port else host
    normalized_url = urlunparse((scheme, netloc, path, "", query or "", ""))
    return normalized_url