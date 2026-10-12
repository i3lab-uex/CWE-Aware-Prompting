import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully‑qualified domain names that are considered trusted.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression for detecting private IP ranges.
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.|                                   # 10.0.0.0/8
        127\.|                                  # 127.0.0.0/8 (loopback)
        169\.254\.|                             # 169.254.0.0/16 (link‑local)
        172\.(1[6-9]|2\d|3[0-1])\.|             # 172.16.0.0/12
        192\.168\.|                             # 192.168.0.0/16
        ::1$                                    # IPv6 loopback
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if *ip* is a private or loopback address."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address; treat as non‑private for safety.
        return False

def _resolve_host(host: str) -> list[str]:
    """Resolve *host* to a list of IP addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        # Host could not be resolved; treat as invalid.
        return []

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL, ensuring it originates from a trusted provider
    and does not resolve to any internal network address.

    Parameters:
        rss_link (str): The raw RSS feed URL.

    Returns:
        str: A sanitized, trusted feed URL.

    Raises:
        ValueError: If the URL is not from a trusted provider or resolves
                    to an internal IP address.
    """
    if not rss_link:
        raise ValueError("Empty URL provided")

    # Parse the URL and ensure it has a scheme.
    parsed = urlparse(rss_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {rss_link}")

    # Enforce HTTPS for external providers.
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # Normalize host (lowercase, strip port if present).
    host = parsed.hostname.lower()
    if not host:
        raise ValueError(f"Could not extract hostname from URL: {rss_link}")

    # Reject URLs that target private IPs directly.
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Ensure the host is in the list of trusted providers.
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host}")

    # Resolve the host to IP addresses and check each one.
    resolved_ips = _resolve_host(host)
    if not resolved_ips:
        raise ValueError(f"Could not resolve host: {host}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private")

    # Reconstruct the URL to ensure consistent formatting.
    sanitized = urlunparse((
        "https" if scheme == "http" else scheme,  # force https for http
        host,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return sanitized

# Example usage (for testing only; remove or comment out in production):
if __name__ == "__main__":
    test_urls = [
        "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "http://localhost/feed",  # should raise ValueError
    ]

    for url in test_urls:
        try:
            print("Original:", url)
            print("Sanitized:", clean_feed_link(url))
        except ValueError as e:
            print("Error:", e)
        print("-" * 40)