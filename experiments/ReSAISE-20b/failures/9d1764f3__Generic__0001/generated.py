import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Whitelisted public API domains (exact matches or subdomains)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "api.secure.com",
    # Add more domains as needed
}

# Regular expression to extract the hostname from a URL
HOSTNAME_RE = re.compile(r"^(?P<scheme>https?)://(?P<host>[^:/]+)(?::(?P<port>\d+))?")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host_to_ips(host: str) -> list[str]:
    """Resolve a hostname to its IP addresses."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {host}")

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a sanitized URL
    suitable for internal API calls.

    Parameters
    ----------
    webhook_link : str
        External webhook URL to validate.

    Returns
    -------
    str
        The original URL if it passes all validation checks.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or resolves to a private IP.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    # Parse the URL
    parsed = urlparse(webhook_link)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against the whitelist
    if host not in WHITELISTED_DOMAINS:
        # Allow subdomains of whitelisted domains
        if not any(host.endswith("." + domain) for domain in WHITELISTED_DOMAINS):
            raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_host_to_ips(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP address: {ip}")

    # Reconstruct the URL to ensure no query string or fragment is included
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "", "", "", "")
    )
    return sanitized