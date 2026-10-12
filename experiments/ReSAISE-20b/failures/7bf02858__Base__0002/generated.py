import re
from urllib.parse import urlparse, urlunparse
import socket
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of approved API endpoints (scheme://host[:port] or just host)
APPROVED_ENDPOINTS = {
    "https://api.example.com",
    "https://internal.api.company.com:8443",
    "example.org",  # host only
}

# Regular expression to detect private, loopback or link-local IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.|169\.254\."
    r"|127\.|::1$|fc00:|fd00:)",
    re.IGNORECASE
)

def _is_ip_private(ip_str: str) -> bool:
    """
    Return True if the given IP string is a private, loopback, or link‑local address.
    """
    try:
        ip_obj = ip_address(ip_str)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host_to_ips(host: str) -> set[str]:
    """
    Resolve a hostname to all associated IP addresses.
    """
    try:
        return {addr[4][0] for addr in socket.getaddrinfo(host, None)}
    except socket.gaierror:
        return set()

def _is_host_allowed(host: str) -> bool:
    """
    Check if the host is in the approved list or resolves to an allowed IP.
    """
    # Direct match against approved endpoints (host only)
    if host in APPROVED_ENDPOINTS:
        return True

    # Check if the host matches any approved endpoint when combined with scheme
    for ep in APPROVED_ENDPOINTS:
        parsed = urlparse(ep)
        if parsed.netloc == host or parsed.path == host:
            return True

    # Resolve DNS and verify IPs are not private
    ips = _resolve_host_to_ips(host)
    if not ips:
        return False

    for ip in ips:
        if _is_ip_private(ip):
            return False
    return True

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL against approved API endpoints and internal network restrictions.

    Args:
        hook_url: The raw URL string provided by an external service.

    Returns:
        A sanitized, validated URL that references an approved API endpoint.

    Raises:
        ValueError: If the URL's domain is not approved or points to a private/internal address.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IPs or internal hostnames
    if _is_ip_private(host):
        raise ValueError("URL resolves to a private IP address")

    # Resolve host and validate
    if not _is_host_allowed(host):
        raise ValueError(f"Host '{host}' is not in the list of approved endpoints")

    # Reconstruct a clean URL (remove userinfo, fragments)
    cleaned = parsed._replace(netloc=f"{host}:{parsed.port}" if parsed.port else host,
                              username=None, password=None,
                              fragment="")
    return urlunparse(cleaned)

# Example usage (would normally be in tests or application code)
if __name__ == "__main__":
    try:
        safe_url = process_hook("https://api.example.com/v1/notify?token=abc")
        print(f"Validated URL: {safe_url}")
    except ValueError as e:
        print(f"Invalid webhook URL: {e}")