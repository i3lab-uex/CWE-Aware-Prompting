import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of trusted feed providers (hostnames)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.reuters.com",
    # Add more trusted providers as needed
}

# Private IP ranges that should never be accessed (CWE‑918 mitigation)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # unique local address
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Invalid IP address
        return True  # treat as private to be safe
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The user supplied RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, trusted URL suitable for fetching.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or resolves to a private IP.
    """
    if not isinstance(feed_address, str):
        raise ValueError("Feed address must be a string")

    parsed = urlparse(feed_address.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Normalize hostname (lowercase) for comparison
    hostname = hostname.lower()

    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Resolve hostname to IP(s) and check for private addresses
    try:
        # Use getaddrinfo to support IPv4 & IPv6
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host {hostname}") from exc

    for entry in addr_info:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Host {hostname} resolves to a private IP ({ip})")

    # Reconstruct the URL with normalized components
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return sanitized

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_feed_source("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
#     except ValueError as e:
#         print("Validation failed:", e)