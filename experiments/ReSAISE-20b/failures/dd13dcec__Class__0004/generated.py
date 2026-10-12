import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully qualified domain names that are considered trusted providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
}

# Regular expression to detect private or loopback IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                               # start non-capturing group for the whole IP
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if the host resolves to a private or loopback IP address."""
    try:
        # Resolve IPv4 and IPv6 addresses
        for addr in ipaddress.ip_address(host):
            if addr.is_private or addr.is_loopback:
                return True
    except ValueError:
        # If host is not an IP address, try to resolve via the socket module
        import socket

        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                infos = socket.getaddrinfo(host, None, family)
                for _, _, _, _, sockaddr in infos:
                    ip = sockaddr[0]
                    if PRIVATE_IP_RE.match(ip):
                        return True
            except socket.gaierror:
                continue
    return False

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The original feed URL supplied by a user or upstream component.

    Returns
    -------
    str
        The sanitized, fully qualified URL that can be safely fetched.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, resolves to a private IP,
        or does not belong to one of the trusted providers.
    """
    # Parse URL and enforce HTTPS scheme only
    parsed = urlparse(feed_url)
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise host to lowercase
    netloc = parsed.hostname.lower() if parsed.hostname else ""
    if not netloc:
        raise ValueError("URL must contain a hostname")

    # Reject any URL that resolves to a private IP or loopback address
    if _is_private_ip(netloc):
        raise ValueError("URL resolves to a private or loopback address")

    # Ensure the host is in our whitelist of trusted providers
    if netloc not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {netloc}")

    # Reconstruct the URL, preserving any path/query/fragment
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized