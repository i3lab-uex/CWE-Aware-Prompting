import re
from urllib.parse import urlparse, urlunparse

# List of approved domains. Add or remove as needed.
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",  # example
    "rss.cnn.com",
}

# Regular expressions for private / loopback IP addresses.
PRIVATE_IP_PATTERNS = [
    re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^::1$"),
]

def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private or loopback IP address."""
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True
    return False

def _is_approved_host(host: str) -> bool:
    """Check if the host is in the approved domain list or a public IP."""
    # Reject private IPs
    if _is_private_ip(host):
        return False

    # If host looks like an IP address, allow it if not private
    ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    if ip_pattern.match(host):
        # Accept only public IPs; we already ruled out private ones
        return True

    # Otherwise check against the approved domains list (case-insensitive)
    return host.lower() in APPROVED_DOMAINS

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the given RSS feed URL points to an approved provider.
    
    Parameters
    ----------
    rss_feed_url : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to an approved provider.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an unapproved domain, or attempts to access a private network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url.strip())

    # Basic scheme validation
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    # Remove any userinfo and port for host comparison
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("Could not determine hostname from URL")

    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not an approved provider")

    # Rebuild the URL without userinfo or port to avoid accidental leakage
    sanitized = urlunparse((
        parsed.scheme,
        host,                # netloc without port
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""                   # no fragment
    ))

    return sanitized