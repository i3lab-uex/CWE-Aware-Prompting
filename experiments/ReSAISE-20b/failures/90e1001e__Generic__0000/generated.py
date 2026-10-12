import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved external API domains (add as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.provider.net",
    "openweather.org",
}

# Regex to detect private IP ranges (IPv4 and IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        # 10.0.0.0/8
        (10(?:\.\d{1,3}){3})|
        # 172.16.0.0/12
        (172\.(1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})|
        # 192.168.0.0/16
        (192\.168(?:\.\d{1,3}){2})|
        # 127.0.0.0/8 (loopback)
        (127(?:\.\d{1,3}){3})|
        # IPv6 link-local
        (fe80:(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4})|
        # IPv6 unique local
        (fc00:(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4})|
        # IPv6 loopback
        (::1)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if an IP address is private, loopback or otherwise non‑public.
    """
    try:
        # ipaddress handles both IPv4 and IPv6
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # If parsing fails, fallback to regex (covers malformed strings)
        return bool(PRIVATE_IP_REGEX.match(ip))

def validate_service_url(service_url: str) -> str:
    """
    Validate that a service URL points to an approved external API domain and
    does not resolve to an internal network address.

    Args:
        service_url: The URL string to validate.

    Returns:
        The same URL if it passes validation.

    Raises:
        ValueError: If the URL is not from an approved domain or points to a private IP.
    """
    if not service_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(service_url)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Normalise hostname to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # 1. Check against approved domains
    if host not in APPROVED_DOMAINS:
        # Allow subdomains of approved domains (e.g., api.example.com)
        if not any(host.endswith("." + domain) for domain in APPROVED_DOMAINS):
            raise ValueError(f"Domain '{host}' is not approved")

    # 2. Resolve hostname to IP addresses and ensure none are private
    try:
        import socket

        # Retrieve all IPv4/IPv6 addresses for the host
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Host '{host}' resolves to private IP '{ip}', disallowed for SSRF protection")

    # Reconstruct URL to ensure canonical form
    cleaned_url = urlunparse(parsed._replace(netloc=host + (f":{parsed.port}" if parsed.port else "")))
    return cleaned_url