import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Whitelisted public API endpoints (domain names or subdomains)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public-api.service.org",
    "gateway.company.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}|
        0\.0\.0\.0|255\.255\.255\.255
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved
    except ValueError:
        return False

def _is_whitelisted(hostname: str) -> bool:
    """Check if the hostname matches any of the whitelisted domains."""
    # Direct match
    if hostname in WHITELISTED_DOMAINS:
        return True

    # Subdomain check (e.g., api.example.com -> example.com)
    for domain in WHITELISTED_DOMAINS:
        if hostname.endswith("." + domain):
            return True
    return False

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL before it is used for internal API calls.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL supplied by an upstream component.

    Returns
    -------
    str
        A normalized, validated URL that is safe for internal use.

    Raises
    ------
    ValueError
        If the URL's domain is not whitelisted or resolves to a private/internal IP.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Normalize the URL (remove fragments, default ports)
    normalized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            "",  # params
            parsed.query,
            ""   # fragment
        )
    )

    hostname = parsed.hostname.lower()

    if not _is_whitelisted(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    return normalized