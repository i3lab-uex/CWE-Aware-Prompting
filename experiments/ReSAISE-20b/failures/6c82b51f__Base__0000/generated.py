import socket
from urllib.parse import urlparse, urlunparse

# List of trusted hostnames (case‑insensitive)
TRUSTED_HOSTNAMES = {
    "rss.example.com",
    "feeds.feedburner.com",
    "news.provider.org",
    # Add more trusted providers as needed
}

# Private IP ranges (IPv4 and IPv6) that should not be reachable
PRIVATE_IPV4_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
]
PRIVATE_IPV6_RANGES = [
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
]

def _ip_in_private_range(ip: str) -> bool:
    """Return True if the IP address is within any private range."""
    try:
        # IPv4
        packed_ip = socket.inet_aton(ip)
        ip_int = int.from_bytes(packed_ip, "big")
        for start, end in PRIVATE_IPV4_RANGES:
            if int.from_bytes(socket.inet_aton(start), "big") <= ip_int <= int.from_bytes(socket.inet_aton(end), "big"):
                return True
    except OSError:
        # Not an IPv4 address, try IPv6
        try:
            packed_ip = socket.inet_pton(socket.AF_INET6, ip)
            ip_int = int.from_bytes(packed_ip, "big")
            for start, end in PRIVATE_IPV6_RANGES:
                if int.from_bytes(socket.inet_pton(socket.AF_INET6, start), "big") <= ip_int <= int.from_bytes(socket.inet_pton(socket.AF_INET6, end), "big"):
                    return True
        except OSError:
            # Invalid IP address format
            pass
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL, ensuring it originates from a trusted provider
    and does not resolve to a private/internal network address.

    Parameters:
        rss_link (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or resolves to
                    an internal/private network.
    """
    # Basic URL parsing and scheme check
    parsed = urlparse(rss_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Normalize hostname to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check against trusted hostnames
    if host not in TRUSTED_HOSTNAMES:
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    # Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _ip_in_private_range(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP address ({ip})")

    # Reconstruct the URL without fragments or userinfo for safety
    sanitized = urlunparse((
        parsed.scheme,
        f"{host}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query (RSS feeds may use it)
        ""   # fragment removed
    ))
    return sanitized