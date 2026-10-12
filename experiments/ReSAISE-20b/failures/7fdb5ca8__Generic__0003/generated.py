import re
import socket
import ipaddress
from urllib.parse import urlparse, unquote

# Define a set of trusted domains or domain patterns.
# In production this should be loaded from a secure configuration.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.internal.org",
    # Regex patterns for domains that should be accepted
    r"^api\.trusted-\w+\.com$",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_RE = re.compile(
    r"^(127\.0\.0\.1|"
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"169\.254\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or ip == "127.0.0.1"
    except ValueError:
        return False

def _resolve_host(host: str) -> list[str]:
    """Return a list of IP addresses resolved for the host."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []

def _is_trusted_domain(host: str) -> bool:
    """Check if host matches any trusted domain or pattern."""
    # Exact match
    if host in TRUSTED_DOMAINS:
        return True
    # Pattern match
    for pattern in TRUSTED_DOMAINS:
        if isinstance(pattern, str) and pattern.startswith("^"):
            if re.match(pattern, host):
                return True
    return False

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the given URL points to an external, trusted API endpoint.
    
    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL resolves to a private IP, or if the domain is not trusted.
    """
    parsed = urlparse(url_to_check)
    
    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    host = parsed.hostname.lower()
    
    # Check against trusted domains
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # Resolve host to IP addresses
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    # Reject any private IPs
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or reserved; potential SSRF")

    # Ensure the URL path does not contain suspicious patterns (optional)
    if re.search(r"(\.\./|%2e%2e/)", unquote(parsed.path)):
        raise ValueError("URL path contains directory traversal patterns")

    return url_to_check