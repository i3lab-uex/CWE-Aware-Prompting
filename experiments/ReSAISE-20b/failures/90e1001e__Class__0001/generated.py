import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A list of approved external API domains (add as needed)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.example.com",  # placeholder
}

# Regex to detect IPv4 or IPv6 addresses in a URL
IP_PATTERN = re.compile(
    r"""
    ^(?P<scheme>https?)://               # scheme
    (?P<host>
        \[
            (?P<ipv6>[^]]+)             # IPv6 inside []
          |
            (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3})  # IPv4
          |
            (?P<hostname>[^:/?#]+)      # hostname
        )
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def _normalize_url(parsed: urlparse) -> str:
    """Return a canonical form of the URL."""
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = re.sub(r'/+', '/', parsed.path)  # collapse duplicate slashes
    return urlunparse((scheme, netloc, path, '', '', ''))

def validate_service_url(service_url: str) -> str:
    """
    Validate that a URL points to an approved external API and is not
    targeting an internal or private network address.

    Args:
        service_url: The URL string to validate.

    Returns:
        A canonicalised version of the validated URL.

    Raises:
        ValueError: If the URL does not belong to an approved domain,
                    if it contains a private IP, or if parsing fails.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    # Basic parsing
    parsed = urlparse(service_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to IP(s) and check each
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to private IP address {ip}")

    # Check domain whitelist
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not an approved domain")

    # Return a normalized URL
    return _normalize_url(parsed)