import socket
from urllib.parse import urlparse, urlunparse

# List of trusted provider domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "www.reddit.com",
    "news.google.com",
    # add more trusted providers here
}

# Private IP ranges to block (CIDR notation)
PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),   # loopback
    ("169.254.0.0", "169.254.255.255"), # link local
    ("::1/128", "::ffff:127.0.0.1"),    # IPv6 loopback
]

def _ip_in_range(ip: str, start_ip: str, end_ip: str) -> bool:
    """Check if an IPv4 address falls within a start/end range."""
    ip_int = int.from_bytes(socket.inet_aton(ip), "big")
    start_int = int.from_bytes(socket.inet_aton(start_ip), "big")
    end_int   = int.from_bytes(socket.inet_aton(end_ip),   "big")
    return start_int <= ip_int <= end_int

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    for start, end in PRIVATE_IP_RANGES:
        if _ip_in_range(ip, start, end):
            return True
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or
                    resolves to a private/restricted IP address.
    Returns:
        str: The original, sanitized URL (ensuring scheme is http/https).
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Ensure netloc (hostname) is present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted domains (case‑insensitive)
    if not any(hostname.lower().endswith("." + d) or hostname.lower() == d
               for d in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # Resolve the hostname to IP(s)
    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from None

    # Verify none of the resolved IPs are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # Reconstruct the URL to ensure it is normalized
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower(),
                                            netloc=hostname,
                                            path=parsed.path or "/"))
    return sanitized