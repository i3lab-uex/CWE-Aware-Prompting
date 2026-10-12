import re
import socket
from urllib.parse import urlparse

# List of fully qualified domain names that are allowed to be used as RSS feeds.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "feeds.reuters.com",
    "rss.cnn.com",
}

# Regex pattern to detect private, loopback or link‑local IP addresses
PRIVATE_IP_PATTERNS = [
    re.compile(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)(\d{1,3}\.){2}\d{1,3}$"),
    re.compile(r"^127\.(\d{1,3}\.){2}\d{1,3}$"),
    re.compile(r"^169\.254\.(\d{1,3}\.){2}\d{1,3}$"),
    re.compile(r"^::1$"),                     # IPv6 loopback
    re.compile(r"^fe80:(:.*)?$"),             # IPv6 link‑local
    re.compile(r"^fc00:(:.*)?$"),             # IPv6 unique local
    re.compile(r"^fd00:(:.*)?$"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private, loopback or link‑local range."""
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(ip):
            return True
    return False

def _is_trusted_domain(hostname: str) -> bool:
    """Check if the hostname matches one of the trusted domains."""
    # Normalise to lower case and strip trailing dot if present
    hostname = hostname.lower().rstrip(".")
    return any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS)

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not point
    to an internal network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, not from a trusted domain,
                    or resolves to an internal IP address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    # Basic URL parsing
    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Ensure the hostname is from a trusted provider
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # Resolve hostname to all associated IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    # Check each resolved IP address
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to internal IP address {ip}"
            )

    # If all checks pass, return the original URL
    return source_url