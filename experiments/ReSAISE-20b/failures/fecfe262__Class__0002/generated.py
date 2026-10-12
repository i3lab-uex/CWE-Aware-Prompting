import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A small list of approved RSS feed providers.
# In a real application this could come from a config file or database.
APPROVED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    # add more trusted domains here
}

# Regular expression to detect private or loopback IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.0\.0\.1$)|                       # localhost
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$)|     # 10.0.0.0/8
    (^172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}$)|  # 172.16.0.0/12
    (^192\.168\.\d{1,3}\.\d{1,3}$)|        # 192.168.0.0/16
    (^169\.254\.\d{1,3}\.\d{1,3}$)         # link-local
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or loopback address."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    point to any internal or private network.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed to validate.

    Returns:
        str: A sanitized and validated URL that can be safely fetched.

    Raises:
        ValueError: If the URL is not from an approved provider, points to a
                    private network, or otherwise fails validation.
    """
    if not rss_feed_url:
        raise ValueError("RSS feed URL must not be empty")

    parsed = urlparse(rss_feed_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve IP addresses for the hostname
    try:
        import socket

        addr_info = socket.getaddrinfo(host, None)
        for family, _, _, _, sockaddr in addr_info:
            ip = sockaddr[0]
            if _is_private_ip(ip):
                raise ValueError(f"Hostname resolves to a private IP: {ip}")
    except socket.gaierror as e:
        raise ValueError(f"Could not resolve hostname '{host}': {e}")

    # Check against approved providers
    if host.lower() not in APPROVED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not an approved provider")

    # Rebuild the URL to ensure it has no unexpected components
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://127.0.0.1/feed.xml",
        "https://unknown.com/feed.xml",
    ]

    for url in test_urls:
        try:
            print("Valid:", filter_rss_feed(url))
        except ValueError as e:
            print("Invalid:", url, "->", e)