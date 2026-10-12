import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# A set of approved RSS feed hostnames (including subdomains if needed)
APPROVED_HOSTS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "news.google.com",          # Example of a trusted provider
    "feeds.reuters.com",
}

# Regular expression to detect private IP ranges (RFC 1918, loopback, link-local, etc.)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0/8 (loopback)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 169.254.0.0/16 (link-local)
        (?:169\.254\.\d{1,3}\.\d{1,3})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _hostname_to_ip(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None)
        return [info[4][0] for info in infos]
    except socket.gaierror:
        return []

def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the provided RSS link points to a trusted provider and does not
    resolve to any private/internal IP addresses.

    Parameters:
        rss_link (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized version of the original URL if it is approved.

    Raises:
        ValueError: If the URL is not from an approved provider or attempts to
                    access a restricted internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Basic URL checks
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("RSS link must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("RSS link must contain a network location (host)")

    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("Invalid host in RSS link")

    # Check against approved hosts
    if hostname not in APPROVED_HOSTS:
        raise ValueError(f"Host '{hostname}' is not an approved RSS provider")

    # Resolve hostname to IPs and ensure none are private
    ips = _hostname_to_ip(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # Reconstruct a sanitized URL (lowercase scheme, netloc; preserve path/query/fragment)
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized