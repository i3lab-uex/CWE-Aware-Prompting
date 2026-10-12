import re
from urllib.parse import urlparse

# List of trusted RSS providers (domain names)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.reuters.com",
    "feeds.npr.org",
    "rss.bbc.co.uk",
}

# Regex for private IP ranges (RFC1918 and other reserved ranges)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0/8 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 169.254.0.0/16 (link-local)
        (169\.254\.\d{1,3}\.\d{1,3})|
        # ::1 (IPv6 loopback)
        (::1)|
        # 2001:db8::/32 (documentation)
        (2001:db8(?:[0-9a-fA-F]{0,4}:){0,7}[0-9a-fA-F]{1,4})|
        # 3ffe::/16 (private)
        (3ffe:[0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{1,4}
    )
    """,
    re.VERBOSE,
)


def _is_private_host(host: str) -> bool:
    """
    Detect if the host is a private IP or reserved domain.
    """
    # Directly check IPv4/IPv6 patterns
    if PRIVATE_IP_REGEX.match(host):
        return True

    # Reject localhost aliases
    if host.lower() in {"localhost", "127.0.0.1"}:
        return True

    # Basic check for IPv6 literals
    if re.match(r"^\[.*\]$", host):
        ip = host.strip("[]")
        if PRIVATE_IP_REGEX.match(ip):
            return True

    # If the host is an IP address (numeric), reject if private
    try:
        import ipaddress

        addr = ipaddress.ip_address(host)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a plain IP address; keep checking domain list later
        pass

    return False


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the provided RSS feed URL belongs to an approved provider
    and does not point to a private/internal network.

    Args:
        rss_feed_url: URL of the RSS feed to validate.

    Returns:
        The original URL if it passes validation.

    Raises:
        ValueError: If the URL is not from an approved provider or points to a private network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Ensure host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()
    if _is_private_host(host):
        raise ValueError("URL points to a private or restricted network")

    # Verify that the host ends with one of the trusted domains
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Host '{host}' is not an approved RSS provider")

    # Reconstruct the URL to normalise it
    sanitized_url = parsed.geturl()

    return sanitized_url