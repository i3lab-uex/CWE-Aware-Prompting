import re
import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of approved public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.public.org",
    "data.partner.net",
}

# Regular expression to detect IPv4 or IPv6 addresses in a hostname.
IP_REGEX = re.compile(r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[([0-9a-fA-F:]+)\]
    )$
""", re.VERBOSE)


def _is_private_ip(addr: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    try:
        ip = ip_address(addr)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False


def _validate_hostname(hostname: str) -> None:
    """
    Validate that the hostname is either a public domain from ALLOWED_DOMAINS
    or an IP address not in a private range.
    """
    # Strip port if present
    hostname = hostname.split(":")[0]

    # Check for IP literal
    if IP_REGEX.match(hostname):
        ip_literal = hostname.strip("[]")
        if _is_private_ip(ip_literal):
            raise ValueError(f"IP address {ip_literal} is not allowed (private/loopback).")
        return  # IP literal is acceptable

    # Resolve hostname to IPs (optional, could be skipped for speed)
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP: {ip}")

    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {hostname} is not in the list of allowed public API domains.")


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return a sanitized version that can be used
    for internal API requests.

    Parameters
    ----------
    webhook_address : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated URL that can safely be used for internal API calls.

    Raises
    ------
    ValueError
        If the domain is not in the allowed list or points to a private/internal network.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("webhook_address must be a string")

    parsed = urlparse(webhook_address)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    _validate_hostname(parsed.netloc)

    # Reconstruct the URL to ensure consistent formatting
    cleaned = urlunparse(
        (parsed.scheme, parsed.netloc.lower(), parsed.path or "/", "", "", "")
    )
    return cleaned