#!/usr/bin/env python3
"""
Utility to validate external webhook URLs against a whitelist and ensure they do not point to private networks.
"""

from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (hostnames or IPs)
WHITELIST = {
    "api.example.com",
    "services.public.net",
    "203.0.113.5",          # Example public IP
}

# Public IP ranges that are allowed (RFC 5737 TEST-NET-3)
PUBLIC_IP_RANGES = [
    ipaddress.ip_network("203.0.113.0/24"),
]

# Private IP ranges to block
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _is_public_ip(ip: str) -> bool:
    """
    Determine if an IP address is public (not private or reserved).
    """
    addr = ipaddress.ip_address(ip)
    # Check against private ranges
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return False
    # Optionally allow only specific public ranges; otherwise accept any global address
    for net in PUBLIC_IP_RANGES:
        if addr in net:
            return True
    # Global unicast addresses are considered public
    return addr.is_global

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL against an approved whitelist and ensure it does not target
    internal or private network addresses.

    Parameters:
        webhook_endpoint (str): The external webhook URL to validate.

    Returns:
        str: A sanitized, validated URL safe for internal API usage.

    Raises:
        ValueError: If the URL domain is not in the whitelist or points to a private IP.
    """
    if not webhook_endpoint:
        raise ValueError("Webhook URL cannot be empty")

    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {webhook_endpoint}")

    host = parsed.hostname
    if not host:
        raise ValueError(f"Unable to resolve hostname in URL: {webhook_endpoint}")

    # Resolve host to IP(s) if it's a domain name
    try:
        import socket
        ip_list = socket.getaddrinfo(host, None)
        ips = {entry[4][0] for entry in ip_list}
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {host}: {exc}") from exc

    # Validate each resolved IP
    for ip in ips:
        if not _is_public_ip(ip):
            raise ValueError(f"URL {webhook_endpoint} resolves to a private IP: {ip}")

    # Check against whitelist (by hostname or IP)
    if host not in WHITELIST and all(ip not in WHITELIST for ip in ips):
        raise ValueError(f"Domain {host} is not in the approved whitelist")

    # Reconstruct a sanitized URL (remove query parameters to avoid leaking secrets)
    safe_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return safe_url

# Example usage (commented out for module import safety)
# if __name__ == "__main__":
#     try:
#         print(verify_webhook("https://api.example.com/webhooks/notify?token=abc"))
#     except ValueError as e:
#         print(f"Validation error: {e}")