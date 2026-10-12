import re
from urllib.parse import urlparse, urlunparse
import socket
from ipaddress import ip_address, ip_network

# ----------------------------------------------------------------------
# Configuration: list of trusted RSS providers (domain names)
# ----------------------------------------------------------------------
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Private network ranges (CWE-441 mitigation)
PRIVATE_NETWORKS = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),
    ip_network("169.254.0.0/16"),  # link-local
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is within a private network range."""
    try:
        addr = ip_address(ip)
        return any(addr in net for net in PRIVATE_NETWORKS)
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> set[str]:
    """Resolve the hostname to all associated IPv4 addresses."""
    try:
        return {addr[4][0] for addr in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)}
    except socket.gaierror:
        return set()


def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers and
    ensure it does not resolve to any internal/private network.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider, or if it resolves to a private network.
    """
    # Basic URL parsing and scheme check
    parsed = urlparse(rss_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Normalize hostname to lowercase for comparison
    hostname_lower = hostname.lower()

    # Check if the hostname is in the trusted domain list
    if not any(hostname_lower == domain or hostname_lower.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted provider: {hostname}")

    # Resolve hostname to IP addresses and ensure none are private
    resolved_ips = _resolve_hostname(hostname_lower)
    if not resolved_ips:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to private IP {ip}")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, parsed.fragment)
    )
    return sanitized