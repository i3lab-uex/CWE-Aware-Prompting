import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (fully qualified domain names)
WHITELIST_DOMAINS = {
    "api.example.com",
    "public.service.org",
    "services.vendor.net"
}

# Prefix to prepend for internal API calls
INTERNAL_API_PREFIX = "https://internal-api.company.local/"

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address; treat as non‑private for safety
        return False

def _resolve_domain(domain: str) -> list[str]:
    """Resolve a domain to its IPv4 and IPv6 addresses."""
    try:
        return socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL against a whitelist and ensure it does not
    resolve to private/internal addresses. If valid, return an internal API URL
    that can be safely used for server‑side requests.

    Parameters:
        callback_url (str): The external webhook URL to validate.

    Returns:
        str: A fully‑qualified internal API URL derived from the validated
             external callback.

    Raises:
        ValueError: If the domain is not in the whitelist or resolves to a
                    private/internal IP address.
    """
    if not callback_url:
        raise ValueError("callback_url must be a non‑empty string")

    parsed = urlparse(callback_url)

    # Only allow HTTP/HTTPS schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    domain = parsed.hostname
    if not domain:
        raise ValueError("URL must contain a valid hostname")

    # Enforce whitelist
    if domain not in WHITELIST_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not whitelisted")

    # Resolve the domain and check for private IPs
    addr_info = _resolve_domain(domain)
    if not addr_info:
        raise ValueError(f"Unable to resolve domain: {domain}")

    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Domain '{domain}' resolves to private IP: {ip}")

    # Build the internal API URL (maintain path and query)
    internal_path = parsed.path
    if not internal_path.startswith("/"):
        internal_path = "/" + internal_path

    internal_url_parts = (
        urlparse(INTERNAL_API_PREFIX)._replace(path=internal_path, query=parsed.query).geturl()
    )
    return internal_url_parts