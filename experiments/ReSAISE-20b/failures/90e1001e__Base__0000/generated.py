import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of domains that are explicitly allowed to be called from the server.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "data.provider.net",
}

# Commonly used private IP ranges (RFC 1918, link-local, loopback)
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    addr = ipaddress.ip_address(ip)
    return any(addr in net for net in PRIVATE_NETWORKS)

def validate_service_url(service_url: str) -> str:
    """
    Validate that a URL points to an approved external API and does not resolve
    to any internal/private IP address.

    Parameters:
        service_url (str): The URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    resolves to a disallowed domain or private IP.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)

    # Only http/https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to all IPv4/IPv6 addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # Ensure at least one IP is public
    public_ip_found = False
    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if _is_private_ip(ip_str):
            continue
        public_ip_found = True
        break

    if not public_ip_found:
        raise ValueError(f"Hostname '{hostname}' resolves only to private IP addresses")

    # Verify the hostname is in the approved list
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not an approved domain")

    # Reconstruct the URL to normalise it (e.g., strip default ports)
    normalized_url = urlunparse(parsed._replace(netloc=hostname))
    return normalized_url