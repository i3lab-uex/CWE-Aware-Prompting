import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# A list of approved domain patterns (regular expressions).
# Example: allow only example.com and its subdomains.
ALLOWED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\.trustedpartner\.org$",
]

# Optional: allow a list of exact IP addresses (rare but sometimes needed)
ALLOWED_IPS = set()

# Private / non‑public IP ranges that must be blocked.
PRIVATE_NETWORKS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),   # Unique local address
    ipaddress.IPv6Network("fe80::/10"),  # Link‑local address
]

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP is in a private/non‑public network."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # Invalid IP – treat as unsafe
    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False

def _is_domain_allowed(host: str) -> bool:
    """Check if the hostname matches one of the allowed patterns."""
    for pattern in ALLOWED_DOMAIN_PATTERNS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False

def _resolve_host(host: str) -> set[str]:
    """
    Resolve a hostname to all IPv4/IPv6 addresses.
    Returns a set of string IPs. If resolution fails, returns an empty set.
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return set()
    ips = {addr[4][0] for addr in infos}
    return ips

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the given URL points to an approved external API endpoint.
    
    Raises:
        ValueError: If the host is not allowed or resolves to a private IP.
    
    Returns:
        str: The original URL if it passes validation.
    """
    parsed = urlparse(endpoint_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 1. Check domain against whitelist
    if not _is_domain_allowed(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # 2. Resolve hostname to IPs
    resolved_ips = _resolve_host(host)
    if not resolved_ips:
        raise ValueError(f"Could not resolve hostname: {host}")

    # 3. Ensure none of the IPs are private or in ALLOWED_IPS
    for ip in resolved_ips:
        if ip in ALLOWED_IPS:
            continue  # Explicitly allowed IP
        if _is_ip_private(ip):
            raise ValueError(f"Resolved IP {ip} is in a private network")

    # 4. (Optional) Re‑assemble the URL to normalize it
    normalized = urlunparse(parsed._replace(netloc=host))
    return normalized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = check_api_endpoint("https://api.example.com/v1/resource")
        print(f"Verified URL: {safe_url}")
    except ValueError as exc:
        print(f"URL rejected: {exc}")