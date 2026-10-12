import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (netlocs). Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com/rss",
    "rss.cnn.com",
    # ... add more trusted domains here
}

# Regex to match private IP addresses and local network ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^|\.)  # start of string or dot separator
    (?:
        10\.          # 10.0.0.0/8
      | 172\.(?:1[6-9]|2\d|3[0-1])\.  # 172.16.0.0/12
      | 192\.168\.          # 192.168.0.0/16
      | 127\.)              # localhost
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is in a private or loopback range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address, treat as non-private
        return False

def _is_blocked_host(host: str) -> bool:
    """Check if host resolves to a private IP or is explicitly blocked."""
    # Simple regex check for obvious private ranges
    if PRIVATE_IP_REGEX.search(host):
        return True

    # Resolve hostname to IPs and check for private addresses
    try:
        import socket
        ips = socket.getaddrinfo(host, None)
        for _, _, _, _, sockaddr in ips:
            ip = sockaddr[0]
            if _is_private_ip(ip):
                return True
    except Exception:
        # If DNS resolution fails, be conservative and block
        return True

    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL suitable for fetching.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, points to a private network,
        or uses an unsupported scheme.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Only allow HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Block any attempt to access private networks
    if _is_blocked_host(parsed.hostname):
        raise ValueError("URL points to a private or blocked network")

    # Ensure the host is in the trusted providers list
    if parsed.hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Host '{parsed.hostname}' is not a trusted provider")

    # Reconstruct the URL to ensure it is normalized
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query parameters (e.g., feeds with ?format=xml)
        "",  # fragment
    ))

    return sanitized