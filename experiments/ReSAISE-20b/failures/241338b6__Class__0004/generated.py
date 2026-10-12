import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A whitelist of domains that are considered trustworthy
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.example.com",          # add your own domains here
}

# Private IP ranges (CVE-441 related)
PRIVATE_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fd00::/8"),
    ipaddress.IPv6Network("fe80::/10"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    addr = ipaddress.ip_address(ip)
    return any(addr in net for net in PRIVATE_RANGES)

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to its IPv4/IPv6 addresses.
    Returns a list of IP strings or raises socket.gaierror if resolution fails.
    """
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    return list({sock[4][0] for sock in infos})  # deduplicate

def verify_api_link(url_to_check: str) -> str:
    """
    Verify that a URL points to an approved external API and does not resolve
    to any private/internal IP address.

    Parameters:
        url_to_check (str): The URL to validate.

    Returns:
        str: The original URL if it is considered safe.

    Raises:
        ValueError: If the domain is not approved or resolves to a private IP.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Ensure the domain is in the whitelist
    host = parsed.hostname.lower()
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve the hostname and check each IP
    try:
        resolved_ips = _resolve_host(host)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for {host}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private; potential SSRF")

    # Reconstruct the URL to ensure it has a standard form
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url