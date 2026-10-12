import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelist of trusted RSS providers (domain names)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to validate a simple URL structure
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<netloc>(?:[a-zA-Z0-9.-]+|\[[0-9a-f:.]+\]))"
    r"(?P<path>/.*)?$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is private, loopback or reserved.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Invalid IP address; treat as unsafe
        return True

def _resolve_to_ip(host: str) -> list[str]:
    """
    Resolve a hostname to all its IP addresses.
    """
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    resolve to a private/internal IP address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP,
                    resolves to an untrusted domain, or points to a private IP.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    # Basic syntax check
    match = _URL_RE.match(source_url)
    if not match:
        raise ValueError(f"Malformed URL: {source_url}")

    scheme = match.group("scheme").lower()
    netloc = match.group("netloc")
    path = match.group("path") or ""

    # Enforce HTTPS for safety
    if scheme != "https":
        raise ValueError("Only https:// URLs are allowed")

    # Normalise hostname (case-insensitive)
    host = netloc.lower()

    # Strip port if present
    if ":" in host:
        host, _ = host.split(":", 1)

    # Check against trusted providers
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host}")

    # Resolve hostname to IP addresses
    ips = _resolve_to_ip(host)
    if not ips:
        raise ValueError(f"Could not resolve host: {host}")

    # Ensure none of the resolved IPs are private/internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to a private IP: {ip}")

    # Reconstruct the URL to ensure consistent formatting
    cleaned_url = urlunparse((scheme, netloc, path, "", "", ""))
    return cleaned_url