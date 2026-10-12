import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved API endpoints (scheme+netloc). Adjust as needed.
APPROVED_ENDPOINTS = {
    "https://api.example.com",
    "https://internal-api.example.org",
}

# Regex to detect IPv4 or IPv6 literals in URLs
IP_LITERAL_RE = re.compile(r"^\[?(?:[0-9a-fA-F:.]+)\]?$")


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or link‑local."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved internal API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it resolves to an internal network location.
    """
    # Parse the incoming URL
    parsed = urlparse(hook_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Reconstruct the base endpoint (scheme + netloc) for comparison
    base_endpoint = f"{parsed.scheme}://{parsed.netloc}"
    if base_endpoint not in APPROVED_ENDPOINTS:
        raise ValueError(f"Domain {parsed.netloc} is not approved")

    # Prevent host header injection by ensuring hostname matches netloc
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Detect IP literal in the URL
    if IP_LITERAL_RE.match(hostname):
        ip = hostname.strip("[]")
        if _is_private_ip(ip):
            raise ValueError(f"IP {ip} is a private address")
    else:
        # Resolve hostname to IPs and check for private addresses
        ips = _resolve_hostname(hostname)
        if any(_is_private_ip(ip) for ip in ips):
            raise ValueError(f"Hostname {hostname} resolves to a private IP")

    # Build the sanitized URL (preserve path, params, query, fragment)
    safe_url = urlunparse(parsed)

    return safe_url