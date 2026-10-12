import re
from urllib.parse import urlparse, unquote
import ipaddress

# Pre‑approved public API endpoints (example domains)
ALLOWED_DOMAINS = {
    "api.example.com",
    "data.provider.org",
    "services.partner.net"
}

# Regex to detect private IP ranges (RFC 1918, loopback, link‑local)
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.)|                # Loopback
    (^10\.)|                 # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\.)|  # Class B private
    (^192\.168\.)|           # Class C private
    (^169\.254\.)            # Link‑local
    """,
    re.VERBOSE
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If not a valid IP, treat as non‑private (e.g., domain name)
        return False

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL ensuring it points to an approved public API endpoint
    and does not resolve to any private or internal IP address.

    Parameters:
        webhook_url (str): The URL provided by an external service.

    Returns:
        str: A validated, normalized URL that points to a pre‑approved endpoint.

    Raises:
        ValueError: If the domain is not approved or resolves to a private IP.
    """
    if not webhook_url:
        raise ValueError("URL must not be empty")

    parsed = urlparse(webhook_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Normalise domain (case‑insensitive)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Check against whitelist
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an approved endpoint")

    # Resolve the hostname to IPs and ensure none are private
    try:
        import socket
        addrinfos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for family, _, _, _, sockaddr in addrinfos:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Endpoint resolves to private IP '{ip}'")

    # Re‑build the URL with a normalized path and query
    normalized_path = unquote(parsed.path or "/")
    normalized_query = parsed.query
    normalized_fragment = ""  # discard fragments

    return f"{parsed.scheme}://{hostname}{normalized_path}" + (
        f"?{normalized_query}" if normalized_query else ""
    )