import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# Trusted providers list (example domains). Adjust as needed.
_TRUSTED_DOMAINS = {
    "news.ycombinator.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
    "news.google.com",
}

# Private IP ranges to block (CWE‑918 mitigation)
_PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fe80::/10"),  # link local
]

def _is_private_ip(ip: str) -> bool:
    """Check if an IP address falls into a private range."""
    addr = ipaddress.ip_address(ip)
    return any(addr in net for net in _PRIVATE_IP_RANGES)

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to IP addresses, returning a list."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL ensuring it is from a trusted provider
    and does not resolve to a private or internal network address.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated URL ready for fetching.

    Raises:
        ValueError: If the URL is not from a trusted provider or
                    resolves to a private/internal IP address.
    """
    # Basic parsing and scheme check
    parsed = urlparse(rss_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted domains
    if hostname.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Hostname {hostname} is not a trusted provider")

    # Resolve hostname to IP addresses
    ip_list = _resolve_hostname(hostname)
    if not ip_list:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    # Ensure none of the IPs are private/internal
    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")

    # Reconstruct sanitized URL (remove query/fragment if desired)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )
    return safe_url