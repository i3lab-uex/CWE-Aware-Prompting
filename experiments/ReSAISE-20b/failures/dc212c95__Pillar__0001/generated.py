import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.io",
    "webhook.provider.net",
}

# Regular expression to validate URL scheme
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address is private, loopback or link-local.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False


def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to all its IPv4 and IPv6 addresses.
    """
    try:
        return [
            result[4][0]
            for result in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        ]
    except socket.gaierror:
        # Unable to resolve hostname
        return []


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    The function ensures that the URL uses HTTPS, points to one of the
    approved public API domains, and does not resolve to an internal or
    private IP address. If the URL is valid, it is returned unchanged.
    Otherwise a ValueError is raised.

    Args:
        webhook_endpoint: The URL string supplied by the external service.

    Returns:
        A validated HTTPS URL suitable for internal API requests.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS, if the
                    scheme is not HTTPS, or if the resolved IP addresses
                    are private/internal.
    """
    # Ensure scheme is HTTPS
    if not _SCHEME_RE.match(webhook_endpoint):
        raise ValueError("Webhook URL must use HTTPS")

    parsed = urlparse(webhook_endpoint)

    # Domain check
    domain = parsed.hostname.lower() if parsed.hostname else ""
    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an approved webhook endpoint")

    # Resolve hostname to IP addresses
    ip_addresses = _resolve_host(domain)
    if not ip_addresses:
        raise ValueError(f"Unable to resolve domain '{domain}'")

    # Ensure no IP is private or internal
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Domain '{domain}' resolves to private IP address {ip}")

    # Reconstruct the URL to ensure no query params or fragments that could
    # be abused; keep path, scheme and netloc only.
    safe_url = urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))

    return safe_url