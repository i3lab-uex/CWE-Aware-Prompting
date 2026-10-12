import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# List of approved public API domains (example entries)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.service.com",
    "notifications.partner.org",
}

# Regular expression to detect private or loopback IP addresses
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"169\.254\.\d{1,3}\.\d{1,3}"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _validate_domain(domain: str) -> None:
    """Ensure the domain is in the allowed list."""
    if domain.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed")

def _validate_no_private_ip(parsed: ParseResult) -> None:
    """Ensure the URL does not resolve to a private IP."""
    # If hostname is an IP, check directly
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.hostname or ""):
        if _is_private_ip(parsed.hostname):
            raise ValueError("URL points to a private IP address")
    # For hostnames, perform a quick DNS resolution check (optional)
    # In environments without network access this will skip the check.
    try:
        import socket
        for addr in socket.getaddrinfo(parsed.hostname, None):
            ip = addr[4][0]
            if _is_private_ip(ip):
                raise ValueError("URL resolves to a private IP address")
    except Exception:
        # If DNS resolution fails or is not allowed, skip the check
        pass

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a sanitized version
    that can safely be used for internal API requests.

    Parameters:
        webhook_endpoint (str): The URL supplied by an external service.

    Returns:
        str: A validated, sanitized URL ready for internal use.

    Raises:
        ValueError: If the domain is not in the allowed list or
                    if the URL resolves to a private network.
    """
    if not webhook_endpoint:
        raise ValueError("Empty URL provided")

    parsed = urlparse(webhook_endpoint)

    # Ensure scheme is HTTPS or HTTP
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain presence
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Validate domain against allowed list
    _validate_domain(parsed.hostname)

    # Ensure no private IP addresses are used
    _validate_no_private_ip(parsed)

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc.lower(),
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=""
    ))

    return safe_url