import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelisted providers (example domains).  Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regular expression for private / reserved IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3}) |           # 10.0.0.0 – 10.255.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}) |# 172.16.0.0 – 172.31.255.255
        (192\.168\.\d{1,3}\.\d{1,3}) |               # 192.168.0.0 – 192.168.255.255
        (169\.254\.\d{1,3}\.\d{1,3}) |               # 169.254.0.0 – 169.254.255.255
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3}) |           # 127.0.0.0 – 127.255.255.255
        (fc00::/7) |                                 # Unique local address
        (fe80::/10)                                  # Link-local address
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private/reserved address."""
    return PRIVATE_IP_RE.match(ip) is not None

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        return [info[4][0] for info in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    The function ensures that the supplied URL resolves to a public IP address
    and that its hostname belongs to an approved list of providers.

    Args:
        rss_url: The RSS feed URL supplied by the caller.

    Returns:
        A sanitized, validated RSS feed URL that can be safely fetched.

    Raises:
        ValueError: If the URL is not from a trusted provider or points to
            a private/reserved IP address.
    """
    # Basic parsing and scheme validation
    parsed = urlparse(rss_url.strip())
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalise the hostname for comparison
    hostname_lower = hostname.lower()

    if hostname_lower not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not an approved provider")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    # Ensure none of the IPs are private/reserved
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' is private or reserved")

    # Reconstruct a sanitized URL (remove query parameters, fragments)
    sanitized = urlunparse((
        parsed.scheme,
        f"{parsed.netloc}",
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    ))
    return sanitized

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         print(secure_feed_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
#     except ValueError as e:
#         print(f"Validation failed: {e}")