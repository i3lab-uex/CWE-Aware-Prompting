import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A simple list of approved domains or domain patterns.
# This can be expanded as needed.
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^services\.trusted\.org$",
]

# Regex for detecting localhost or loopback
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)


def _is_approved_domain(domain: str) -> bool:
    """Check if the domain matches one of the approved patterns."""
    for pattern in APPROVED_DOMAINS:
        if re.match(pattern, domain):
            return True
    return False


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str):
    """Resolve hostname to all IP addresses."""
    try:
        return socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that the provided URL points to a secure, external API endpoint.

    Raises ValueError if:
        - The scheme is not HTTPS.
        - The host is localhost or a private IP.
        - The domain is not in the approved list.
    Returns:
        The original URL if it passes all checks.
    """
    parsed = urlparse(endpoint_url)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("URL scheme must be HTTPS")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 2. Check for localhost or loopback
    if LOCALHOST_RE.match(host):
        raise ValueError("URL points to a localhost address")

    # 3. Resolve hostname to IPs and check for private addresses
    addr_info = _resolve_hostname(host)
    if not addr_info:
        raise ValueError("Unable to resolve hostname")

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to a private IP address: {ip}")

    # 4. Domain approval check
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # 5. Reconstruct the URL to ensure no trailing spaces or newlines
    cleaned = urlunparse(parsed)
    return cleaned