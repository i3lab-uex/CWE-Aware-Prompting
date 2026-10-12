import re
import socket
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted providers
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.bbc.co.uk",
}

# Regular expression to detect private IP ranges (RFC1918)
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(169\.254\.\d{1,3}\.\d{1,3})"
    r")$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is in a private range."""
    return PRIVATE_IP_RE.match(ip) is not None

def _validate_domain(domain: str) -> bool:
    """Check that the domain is in the trusted list."""
    return domain.lower() in TRUSTED_DOMAINS

def _sanitize_url(parsed: urlparse) -> str:
    """Rebuild the URL ensuring scheme is http or https."""
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {scheme}")
    return urlunparse(parsed)

def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate and sanitize.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, attempts to connect
        to an internal network, or uses an unsupported scheme.
    """
    if not rss_link:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(rss_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {rss_link}")

    # Ensure the domain is trusted
    if not _validate_domain(parsed.netloc):
        raise ValueError(f"Untrusted provider: {parsed.netloc}")

    # Resolve the hostname to an IP address
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {parsed.hostname}") from exc

    # Check each resolved IP; if any is private, reject
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to a private IP address: {ip}")

    # Sanitize and return the URL
    return _sanitize_url(parsed)