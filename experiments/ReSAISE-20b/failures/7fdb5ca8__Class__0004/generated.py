import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A simple whitelist of trusted domains or domain patterns.
TRUSTED_DOMAINS = {
    # Exact hostnames
    "api.example.com",
    "service.partner.org",
    # Patterns: any subdomain of trusted domain
    r"^.+\.trusted-api\.net$",
}

# Regular expression for common private IP ranges
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),      # loopback
    ipaddress.ip_network("169.254.0.0/16"),   # link-local
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),         # Unique local address (ULA)
]

# Ensure HTTPS is used for external APIs
REQUIRED_SCHEMES = {"https"}

def _is_trusted_host(host: str) -> bool:
    """
    Return True if host matches any entry in TRUSTED_DOMAINS.
    Supports exact matches and regex patterns.
    """
    for pattern in TRUSTED_DOMAINS:
        if pattern.startswith("r'") and pattern.endswith("'"):
            # It's a regex string literal
            if re.match(pattern[2:-1], host):
                return True
        elif host == pattern:
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """
    Determine if the given IP address string is within any private range.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in net for net in PRIVATE_IP_RANGES)
    except ValueError:
        # Not a valid IP address; not private
        return False

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an external, trusted API endpoint.
    
    Raises:
        ValueError: if the URL is malformed, points to a private/internal
                    address or domain not in the whitelist.
    
    Returns:
        The original URL if it passes all checks.
    """
    # Basic parsing
    parsed = urlparse(url_to_check)
    
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url_to_check}")

    # Enforce HTTPS
    if parsed.scheme.lower() not in REQUIRED_SCHEMES:
        raise ValueError(f"Only HTTPS URLs are allowed: {url_to_check}")

    # Normalize host (lowercase, strip port)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError(f"URL missing hostname: {url_to_check}")

    # Reject obvious internal references
    if host in {"localhost", "127.0.0.1"}:
        raise ValueError(f"Internal host is not allowed: {url_to_check}")

    # Resolve host to IP(s) and check for private addresses
    try:
        import socket
        addr_info = socket.getaddrinfo(host, None)
        for entry in addr_info:
            ip_str = entry[4][0]
            if _is_private_ip(ip_str):
                raise ValueError(f"URL resolves to private IP {ip_str}: {url_to_check}")
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host {host}: {exc}") from exc

    # Check against trusted domain whitelist
    if not _is_trusted_host(host):
        raise ValueError(f"Host {host} is not in the trusted domain list")

    # Reconstruct URL to ensure it hasn't been tampered with
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return cleaned