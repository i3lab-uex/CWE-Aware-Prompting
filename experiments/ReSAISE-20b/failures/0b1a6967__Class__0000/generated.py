import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved top‑level domains or domain patterns
ALLOWED_DOMAINS = [
    r"^api\.example\.com$",   # your API domain
    r"^.*\.trustedpartner\.org$",
]

# Private IP ranges as per RFC1918 and other non‑public addresses
PRIVATE_IP_RANGES = [
    re.compile(r"^10\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^127\."),
    re.compile(r"^169\.254\."),
    re.compile(r"^0\."),
]

# Optional: block known internal services
BLOCKED_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
}

def _is_public_ip(ip: str) -> bool:
    """Return True if the IP address is not in any private range."""
    for pattern in PRIVATE_IP_RANGES:
        if pattern.match(ip):
            return False
    return True

def _is_allowed_domain(host: str) -> bool:
    """Check that the host matches one of the approved patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Validate that a given URL points to an approved, secure external API.

    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, unchanged.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to a private/internal address,
        or does not match any approved domain pattern.
    """
    if not endpoint_address:
        raise ValueError("Empty URL provided")

    parsed = urlparse(endpoint_address)

    # 1. Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 3. Reject obvious internal hostnames
    if host.lower() in BLOCKED_HOSTNAMES:
        raise ValueError(f"Hostname '{host}' is disallowed")

    # 4. Resolve hostname to IP(s) and ensure they are public
    try:
        ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    for _, _, _, _, sockaddr in ips:
        ip = sockaddr[0]
        if not _is_public_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # 5. Ensure the hostname matches an approved pattern
    if not _is_allowed_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of allowed domains")

    # 6. Re‑assemble URL to ensure normalization (optional)
    normalized = urlunparse(parsed._replace(scheme="https"))
    return normalized