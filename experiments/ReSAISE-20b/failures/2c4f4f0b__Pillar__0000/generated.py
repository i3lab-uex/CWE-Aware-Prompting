import re
from urllib.parse import urlparse, unquote
import ipaddress

# A small whitelist of trusted RSS providers.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex to match private IP ranges.
_PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(169\.254\.\d{1,3}\.\d{1,3})|"
    r"(127\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r")$",
    re.IGNORECASE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if the host resolves to a private IP address."""
    try:
        # If host is already an IP, check directly.
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; attempt to resolve.
        try:
            import socket

            addr_info = socket.getaddrinfo(host, None)
            for family, _, _, _, sockaddr in addr_info:
                ip = ipaddress.ip_address(sockaddr[0])
                if ip.is_private or ip.is_loopback:
                    return True
        except Exception:
            pass
    return False


def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    point to internal network addresses.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not source_url:
        raise ValueError("RSS feed URL must be provided")

    # Parse the URL and normalize percent-encoding
    parsed = urlparse(source_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {source_url!r}")

    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError(f"URL does not contain a valid hostname: {source_url!r}")

    # Reject private IPs or hostnames that resolve to them
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private/internal IP address")

    # Reject URLs that contain private IPs in the host part
    if _PRIVATE_IP_RE.match(hostname):
        raise ValueError("URL contains a private IP address")

    # Ensure the hostname ends with one of the trusted domains
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted RSS provider: {hostname!r}")

    # Optionally, ensure the path looks like an RSS feed
    if not parsed.path.lower().endswith((".xml", ".rss", ".atom")):
        # This is a warning rather than a hard reject; keep it optional
        pass

    # Reconstruct the URL to ensure consistent formatting
    safe_url = parsed.geturl()
    return unquote(safe_url)