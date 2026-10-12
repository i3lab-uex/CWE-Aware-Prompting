import re
from urllib.parse import urlparse
import socket

# --------------------------------------------------------------------
# Approved API endpoints (example).  Replace with your real list.
# Each entry can be a domain or a regex pattern matching subdomains.
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^internal\.service\.company\.net$",
]

# Disallowed IP ranges (RFC 1918, loopback, link-local, etc.)
DISALLOWED_IP_RANGES = [
    re.compile(r"^10\."),                    # 10.0.0.0/8
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^127\."),                   # Loopback
    re.compile(r"^169\.254\."),
    re.compile(r"^0\."),                     # Undefined
]

# --------------------------------------------------------------------
def _is_ip_disallowed(ip: str) -> bool:
    """Return True if the IP address falls into a disallowed range."""
    for pattern in DISALLOWED_IP_RANGES:
        if pattern.match(ip):
            return True
    return False


def _is_domain_approved(domain: str) -> bool:
    """Check if the domain matches any approved pattern."""
    for pattern in APPROVED_DOMAINS:
        if re.match(pattern, domain):
            return True
    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved
    public-facing API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL supplied by an external service.

    Returns
    -------
    str
        The validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a disallowed domain/IP or an internal network.
    """
    # Basic URL parsing
    parsed = urlparse(url_hook)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{parsed.hostname}': {exc}") from exc

    # Check each resolved IP
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_ip_disallowed(ip):
            raise ValueError(f"Disallowed internal IP address: {ip}")

    # Validate domain against approved list
    if not _is_domain_approved(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # If all checks pass, return the original URL (or a canonical form)
    return url_hook