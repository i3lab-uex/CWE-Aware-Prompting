import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a whitelist of trusted domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "www.reddit.com",
    "news.google.com",
    "rss.cnn.com",
    # Add more trusted providers as needed
}

# Regex to detect private IP addresses or localhost in the hostname part
PRIVATE_IP_RE = re.compile(
    r"""
    ^(localhost|127\.0\.0\.1|::1)$
    |^(10\.)          # 10.0.0.0/8
    |^(172\.(1[6-9]|2[0-9]|3[0-1])\. )   # 172.16.0.0/12
    |^(192\.168\.)   # 192.168.0.0/16
    """,
    re.VERBOSE,
)

def _is_private_hostname(hostname: str) -> bool:
    """Return True if the hostname resolves to a private or loopback address."""
    # Direct match against localhost and common private ranges
    if PRIVATE_IP_RE.match(hostname):
        return True

    # Resolve the hostname to IPs and check each
    try:
        for addr in ipaddress.ip_address(hostname):
            if addr.is_private or addr.is_loopback:
                return True
    except ValueError:
        # hostname is not an IP literal, skip resolution
        pass

    return False


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the RSS feed URL belongs to a trusted provider and does not
    point to internal or private networks.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed to validate.

    Returns:
        str: A sanitized, normalized URL that is guaranteed to be from a
             trusted provider.

    Raises:
        ValueError: If the URL is not from an approved provider or points to
                    a restricted internal network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize hostname to lower case for comparison
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    # Reject private/internal hostnames
    if _is_private_hostname(hostname):
        raise ValueError("URL points to a private or internal network")

    # Reject untrusted domains
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {hostname}")

    # Rebuild the URL to ensure no fragments or query params that might alter content
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized