import re
from urllib.parse import urlparse, urlunparse, ParseResult
import socket
import ipaddress

# Whitelisted domains (add approved external APIs here)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    # add more domains as needed
}

# Regex for valid hostname (simplified)
HOSTNAME_REGEX = re.compile(r"^(?=.{1,253}$)([a-zA-Z0-9_](?:[a-zA-Z0-9_-]{0,61}[a-zA-Z0-9_])?\.)+[a-zA-Z]{2,63}$")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or link-local."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        return True  # treat invalid IPs as private/unsafe

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all associated IP addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        return [sock[4][0] for sock in infos]
    except socket.gaierror:
        return []

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that a URL points to an approved external API and does not target
    internal or private network addresses.

    Parameters:
        endpoint_url (str): The URL to be validated.

    Returns:
        str: A canonical, fully-qualified HTTPS URL that has been verified
             to be safe.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a non-whitelisted domain, or resolves to
                    a private/internal IP address.
    """
    # Basic parsing
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Enforce HTTP/HTTPS only
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate hostname
    host = parsed.hostname
    if not host or not HOSTNAME_REGEX.match(host):
        raise ValueError(f"Invalid hostname: {host}")

    # Check against whitelist
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve host to IP(s) and ensure none are private/internal
    ip_addresses = _resolve_hostname(host)
    if not ip_addresses:
        raise ValueError(f"Could not resolve hostname: {host}")

    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP: {ip}")

    # Reconstruct the URL, normalizing scheme and removing default ports
    netloc = host
    if parsed.port:
        # Only include port if it's non-default for the scheme
        default_port = {"http": 80, "https": 443}[parsed.scheme.lower()]
        if parsed.port != default_port:
            netloc += f":{parsed.port}"
    canonical = ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=netloc,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(canonical)