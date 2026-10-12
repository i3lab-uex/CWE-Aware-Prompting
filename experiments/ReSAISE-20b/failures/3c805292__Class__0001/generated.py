import re
import socket
from urllib.parse import urlparse, urlunparse

# List of fully‑qualified domain names (or regexes) that are considered trusted.
TRUSTED_PROVIDERS = [
    r"^feeds\.cnn\.com$",
    r"^rss\.bbc\.co\.uk$",
    r"^news\.yahoo\.com$",
    r"^rss\.reuters\.com$",
]

# CIDR ranges that represent private/internal networks.
PRIVATE_CIDRS = [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
    "::1/128",
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is within a private network."""
    import ipaddress
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the hostname, or raise if resolution fails."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def _is_trusted_hostname(hostname: str) -> bool:
    """Check that the hostname matches one of the trusted provider patterns."""
    return any(re.match(pattern, hostname) for pattern in TRUSTED_PROVIDERS)

def validate_feed_source(feed_address: str) -> str:
    """
    Validate that the given RSS feed URL is from a trusted provider and does not point to
    an internal network.

    Parameters:
        feed_address (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated URL that can safely be fetched.

    Raises:
        ValueError: If the URL is malformed, from an untrusted provider,
                    or resolves to a private/internal IP address.
    """
    # Basic URL parsing and scheme validation
    parsed = urlparse(feed_address)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https are allowed.")
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname.")

    # Normalize hostname (case‑insensitive for DNS)
    hostname = parsed.hostname.lower()
    if not _is_trusted_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers.")

    # Resolve hostname to IP addresses and ensure none are private
    ip_addresses = _resolve_hostname(hostname)
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address: {ip}")

    # Reconstruct the URL with the validated components
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragment removed for security
    ))
    return sanitized

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://feeds.cnn.com/rss",
        "http://rss.bbc.co.uk/news/world/rss.xml",
        "https://malicious.example.com/feed",   # should raise
        "http://127.0.0.1/rss"                 # should raise
    ]
    for url in test_urls:
        try:
            print(f"Validated: {validate_feed_source(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")