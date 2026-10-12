import re
import socket
from urllib.parse import urlparse
import ipaddress

# Whitelist of approved API endpoints (domains or IPs)
APPROVED_DOMAINS = {
    "api.example.com",
    "internal.api.company.com",
    "https://public-api.service.org",  # full scheme+netloc allowed
}

# Regular expression to match IPv4 and IPv6 addresses in URLs
IP_REGEX = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
    |
        # IPv6
        \[?(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\]?
    )
    $
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address is private or reserved.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IP addresses.
    """
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        return []


def _validate_domain(domain: str) -> bool:
    """
    Check if the domain or full netloc is in the approved list.
    """
    # Direct match
    if domain in APPROVED_DOMAINS:
        return True

    # If the domain is an IP, ensure it resolves to a private address
    if IP_REGEX.match(domain):
        return _is_private_ip(domain)

    # Resolve the domain to IPs and check each
    for ip in _resolve_hostname(domain):
        if not _is_private_ip(ip):
            return True
    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service.

    Returns
    -------
    str
        The safely validated URL.

    Raises
    ------
    ValueError
        If the URL's domain is outside the approved list or resolves to a private IP.
    """
    if not webhook_link:
        raise ValueError("Empty URL provided")

    parsed = urlparse(webhook_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {webhook_link}")

    # Normalize netloc (remove port if present)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Could not parse hostname from: {webhook_link}")

    # Ensure the domain is approved
    if not _validate_domain(host):
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # Reconstruct the URL to avoid any hidden manipulation
    safe_url = parsed._replace(scheme=parsed.scheme, netloc=host).geturl()
    return safe_url