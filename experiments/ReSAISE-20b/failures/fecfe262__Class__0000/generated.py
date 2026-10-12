import re
from urllib.parse import urlparse, urlunparse

# A small list of approved RSS feed providers.
# Extend this list as needed for your environment.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex to detect private IP ranges and localhost
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.0\.0\.1$) |                     # localhost
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$) |     # 10.0.0.0/8
    (^172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}$) |  # 172.16.0.0/12
    (^192\.168\.\d{1,3}\.\d{1,3}$) |       # 192.168.0.0/16
    (^169\.254\.\d{1,3}\.\d{1,3}$)         # link-local
    """,
    re.VERBOSE,
)

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    point to private or internal networks.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed to validate.

    Returns:
        str: The original URL if it passes validation checks.

    Raises:
        ValueError: If the URL is not from an approved provider, uses an
            unsupported scheme, or resolves to a private IP address.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    # Parse the URL
    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise the hostname to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject URLs with no hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or loopback IP addresses
    if PRIVATE_IP_RE.search(host):
        raise ValueError("URL points to a private or internal network")

    # Ensure the host is in the whitelist
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to avoid subtle injection via fragments or params
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.feedburner.com/SomeFeed",
        "https://127.0.0.1/rss.xml",  # should fail
    ]

    for url in test_urls:
        try:
            print(f"Validated: {filter_rss_feed(url)}")
        except ValueError as exc:
            print(f"Rejected: {url} -> {exc}")