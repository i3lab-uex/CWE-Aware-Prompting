import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved API domains (case‑insensitive)
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.org",
    "public.api.net",
}

# Regular expression for detecting private IP address ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is a private or loopback IP."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _is_valid_domain(domain: str) -> bool:
    """Check if domain is in the whitelist."""
    return domain.lower() in PRE_APPROVED_DOMAINS

def _is_internal_address(parsed: "ParseResult") -> bool:
    """Detect if the host resolves to a private IP or is an internal domain."""
    # If hostname looks like an IP address, check it
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", parsed.hostname or ""):
        return _is_private_ip(parsed.hostname)

    # Resolve the domain to IPs (could be stubbed or mocked in tests)
    try:
        import socket
        for addrinfo in socket.getaddrinfo(parsed.hostname, None):
            ip = addrinfo[4][0]
            if _is_private_ip(ip):
                return True
    except Exception:
        # If resolution fails, assume it's not internal (defensive)
        pass
    return False

def process_webhook(webhook_url: str) -> str:
    """
    Validate the provided webhook URL.

    The function ensures that:
      * The URL is a well‑formed HTTP/HTTPS URI.
      * Its domain is in the pre‑approved whitelist.
      * The host does not resolve to a private/internal IP.

    Parameters
    ----------
    webhook_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        The validated and normalized URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a non‑approved domain,
        or resolves to an internal address.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Must have scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must have a scheme and host")

    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Check against whitelist
    if not _is_valid_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Detect internal addresses
    if _is_internal_address(parsed):
        raise ValueError("URL resolves to an internal or private address")

    # Re‑construct the URL to normalize it
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return normalized