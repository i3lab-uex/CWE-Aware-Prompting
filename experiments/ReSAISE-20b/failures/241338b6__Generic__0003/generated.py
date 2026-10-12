import socket
import ipaddress
from urllib.parse import urlparse, unquote

# List of approved external API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    "services.mycompany.org",
}

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private, loopback, or link‑local."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        return True  # Treat invalid IPs as unsafe

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        return list({item[4][0] for item in infos})
    except socket.gaierror:
        return []

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an approved external API.

    Raises:
        ValueError: If the URL does not belong to an approved domain
                    or resolves to a private/internal IP address.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_check)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Domain check (case-insensitive)
    if hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IP(s) and ensure none are private/internal
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to a private/internal IP ({ip})"
            )

    # All checks passed – return the normalized URL
    return parsed.geturl()