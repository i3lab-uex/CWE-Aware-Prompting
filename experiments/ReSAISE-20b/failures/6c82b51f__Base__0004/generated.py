import re
import socket
from urllib.parse import urlparse, urlunparse

# List of allowed hostnames (regex patterns or exact matches)
_TRUSTED_HOST_PATTERNS = [
    r"^feeds\.rss\.nytimes\.com$",
    r"^news\.google\.com$",
    r"^rss\.bbc\.co\.uk$",
    # Add more trusted providers here
]

# Regex to detect private IP addresses (RFC1918, loopback, link-local)
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    r"172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|"
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|"
    r"169\.254\.\d{1,3}\.\d{1,3}"
    r"|"
    r"::1$|fc00:|fd00:"
    r")",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    return _PRIVATE_IP_REGEX.match(ip) is not None

def _is_trusted_host(host: str) -> bool:
    """Check if host matches one of the trusted patterns."""
    for pattern in _TRUSTED_HOST_PATTERNS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be validated.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑trusted provider, or attempts to resolve
        to a private/internal network address.
    """
    # Basic parsing
    parsed = urlparse(rss_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Normalize hostname (lowercase)
    host = parsed.hostname.lower()

    # 1. Check against trusted provider list
    if not _is_trusted_host(host):
        raise ValueError(f"Host '{host}' is not in the list of trusted providers")

    # 2. Resolve hostname to IPs
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # 3. Ensure none of the resolved IPs are private
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private or restricted")

    # 4. Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return sanitized

# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://feeds.rss.nytimes.com/rss",
        "http://news.google.com/rss",
        "https://rss.bbc.co.uk/news/world/rss.xml",
        "http://localhost:8000/feed",  # should fail
    ]
    for url in test_urls:
        try:
            print("Valid:", check_feed_url(url))
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")