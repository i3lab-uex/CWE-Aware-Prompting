import re
import socket
from urllib.parse import urlparse, urlunparse

# List of trusted provider hostnames (exact match or subdomains)
TRUSTED_HOSTNAMES = {
    "feed.example.com",
    "rss.google.com",
    "news.yahoo.com",
}

# Regular expression for allowed schemes
SCHEME_REGEX = re.compile(r"^(https?)$")

# Private IP network ranges (RFC1918, link-local, loopback, etc.)
PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),
    ("169.254.0.0", "169.254.255.255"),
]


def ip_to_int(ip: str) -> int:
    """Convert dotted IP string to integer."""
    return sum(int(part) << (8 * i) for i, part in enumerate(reversed(ip.split("."))))


def is_private_ip(ip: str) -> bool:
    """Check if an IP address falls within a private range."""
    ip_int = ip_to_int(ip)
    for start, end in PRIVATE_IP_RANGES:
        if ip_to_int(start) <= ip_int <= ip_to_int(end):
            return True
    return False


def resolve_host(hostname: str) -> list[str]:
    """Resolve hostname to a list of IPv4 addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror:
        return []
    return [info[4][0] for info in infos]


def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL scheme is not https/http, hostname is not trusted,
        or if resolution leads to a private IP address.
    """
    # Parse the URL
    parsed = urlparse(rss_url)
    if not SCHEME_REGEX.match(parsed.scheme):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Hostname must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted hostnames (exact or subdomain)
    if not any(
        hostname == t or hostname.endswith("." + t) for t in TRUSTED_HOSTNAMES
    ):
        raise ValueError("Hostname is not from a trusted provider")

    # Resolve hostname to IPs and ensure none are private
    ips = resolve_host(hostname)
    if not ips:
        raise ValueError("Unable to resolve hostname")
    for ip in ips:
        if is_private_ip(ip):
            raise ValueError("Hostname resolves to a private IP address")

    # Reconstruct the URL to strip any unsafe components (e.g., fragments)
    sanitized = urlunparse(
        (
            parsed.scheme,
            f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
            parsed.path or "/",
            "",  # params
            parsed.query,  # keep query
            "",  # fragment
        )
    )
    return sanitized


# Example usage (uncomment to test):
# print(secure_feed_link("https://feed.example.com/rss.xml"))