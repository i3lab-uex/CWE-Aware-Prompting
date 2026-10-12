import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "cdn.example.net",
}

# Regular expression to match private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    (?:^127\.)|                                   # loopback
    (?:^10\. )|                                   # Class A private
    (?:^172\.(1[6-9]|2\d|3[0-1])\. )|            # Class B private
    (?:^192\.168\.)|                             # Class C private
    (?:^169\.254\.)                              # link-local
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or link‑local."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw user supplied URL.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, the domain is not approved,
        or if the resolved IP address is private / loopback.
    """
    # Parse URL
    parsed = urlparse(input_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Normalize hostname (lowercase)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirects")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    # Ensure all resolved IPs are public
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for domain '{hostname}' is not public")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urlunparse((
        parsed.scheme,
        f"{hostname}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return safe_url