import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved RSS feed providers (domain names only)
ALLOWED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "www.reddit.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
    "www.theguardian.com",
    "news.yahoo.com",
    "rss.slashdot.org",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.          # 10.0.0.0 – 10.255.255.255
    |^172\.1[6-9]\.|^172\.2[0-9]\.|^172\.3[01]\.  # 172.16.0.0 – 172.31.255.255
    |^192\.168\.)   # 192.168.0.0 – 192.168.255.255
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Check if a hostname resolves to a private IP address.
    This function only checks the literal host string; for DNS resolution
    you would need to resolve the hostname which is out of scope here.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private
    except ValueError:
        # Not an IP literal, assume not private (could be a hostname)
        return False

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the provided RSS feed URL points to an approved provider
    and does not target internal networks.

    Parameters:
        rss_feed_url (str): The URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is not from an approved provider or
                    attempts to access a restricted internal network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Normalise host to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject localhost and loopback addresses
    if host in {"localhost", "127.0.0.1"} or _is_private_ip(host):
        raise ValueError("Access to local or private network addresses is forbidden")

    # Reject IP literals that are not allowed
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        # IP literal; check if it is in private range
        try:
            ip_obj = ipaddress.ip_address(host)
            if ip_obj.is_private or ip_obj.is_loopback:
                raise ValueError("Access to private IP addresses is forbidden")
        except ValueError:
            pass  # Not a valid IP; ignore

    # Verify the host is in the list of approved providers
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Provider '{host}' is not approved for RSS feeds")

    # Reconstruct the URL to ensure it remains well‑formed
    sanitized = urlunparse(parsed)
    return sanitized

# Example usage (commented out to keep module import clean):
# if __name__ == "__main__":
#     try:
#         print(filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")