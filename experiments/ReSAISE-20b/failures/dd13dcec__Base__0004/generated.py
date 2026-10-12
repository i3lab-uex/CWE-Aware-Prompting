import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS feed providers (domain names)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex to detect IP addresses (IPv4 or IPv6)
_IP_RE = re.compile(r"""
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[
            (?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}
        \]
    )
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address (IPv4 or IPv6)."""
    # Strip brackets for IPv6 literal
    host = host.strip("[]")
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_private_ip(host: str) -> bool:
    """Return True if the host resolves to a private IP."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate an RSS feed URL ensuring it points to a trusted provider and
    does not attempt SSRF.

    Parameters
    ----------
    feed_url : str
        The URL to validate.

    Returns
    -------
    str
        The sanitized, validated URL.

    Raises
    ------
    ValueError
        If the URL is not trusted, uses an unsafe scheme,
        or attempts to access a private IP/network.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Only http/https schemes are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with empty netloc (e.g., file:// or data:)
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Reject IP addresses or private ranges
    host = parsed.hostname
    if host is None:
        raise ValueError("Invalid URL hostname")

    # Handle IPv6 literal
    host_clean = host.strip("[]")

    if _is_ip_address(host_clean):
        raise ValueError("IP addresses are not allowed in feed URLs")

    if _is_private_ip(host_clean):
        raise ValueError("Private network addresses are not allowed")

    # Ensure host is in the whitelist
    if host_clean.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Host '{host_clean}' is not a trusted RSS provider")

    # Reconstruct the URL to normalise it
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://127.0.0.1/feed",           # should fail
        "ftp://rss.nytimes.com/feed.xml",   # should fail
    ]

    for url in test_urls:
        try:
            print("Valid:", sanitize_feed_url(url))
        except ValueError as e:
            print("Invalid:", url, "->", e)