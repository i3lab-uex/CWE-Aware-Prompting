import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Whitelisted domains (exact match or suffix)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "api.otherdomain.org",
    # Add more approved domains here
}

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or otherwise non‑public."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    Returns a list of string IPs. Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns a list of (family, type, proto, canonname, sockaddr)
        # sockaddr is a tuple where the first element is the IP string
        infos = socket.getaddrinfo(host, None)
        return sorted({sock[4][0] for sock in infos})
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

def verify_api_link(url_to_check: str) -> str:
    """
    Verify that a URL points to an approved external API and is not targeting
    internal or private network addresses.

    Parameters:
        url_to_check (str): The URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL does not belong to an approved domain,
                    resolves to a private IP, or fails any validation.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url_to_check}")

    host = parsed.hostname
    if not host:
        raise ValueError(f"Unable to determine hostname from URL: {url_to_check}")

    # Check against whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Resolve host to IP addresses
    ip_addresses = _resolve_host(host)

    # Ensure none of the resolved IPs are private or internal
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or internal")

    # Rebuild the URL to ensure canonical form
    sanitized_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))

    return sanitized_url