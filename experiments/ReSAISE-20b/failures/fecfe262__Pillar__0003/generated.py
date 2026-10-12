import re
from urllib.parse import urlparse, urlunparse

# List of approved providers (netlocs). Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "feeds.feedburner.com",
    "rss.cnn.com",
    "news.google.com/rss",
    "feeds.feedburner.com/yourblog",  # example of a custom feed
}

# Regex to detect private/internal IP addresses (RFC1918 ranges)
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:                                 # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |    # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0 – 172.31.255.255
        192\.168\.\d{1,3}\.\d{1,3} |      # 192.168.0.0 – 192.168.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |   # loopback
        169\.254\.\d{1,3}\.\d{1,3}         # link-local
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_trusted_netloc(netloc: str) -> bool:
    """Check if the netloc is in the trusted provider list."""
    return netloc.lower() in TRUSTED_PROVIDERS

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the provided RSS feed URL is from an approved provider
    and does not point to a private or internal network.

    Parameters:
        rss_feed_url (str): The URL of the RSS feed to validate.

    Returns:
        str: A sanitized and validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider,
                    uses an insecure scheme, or points to a private IP.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    # Parse the URL
    parsed = urlparse(rss_feed_url)

    # Enforce https or http
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(parsed.netloc.split(":")[0]):
        raise ValueError("URL points to a private or internal IP address")

    # Validate against trusted providers
    if not _is_trusted_netloc(parsed.netloc):
        raise ValueError(f"Untrusted RSS feed provider: {parsed.netloc}")

    # Reconstruct a clean URL (remove fragment and params if any)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            ""   # fragment
        )
    )

    return cleaned

# Example usage (commented out for safety)
# try:
#     safe_url = filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(safe_url)
# except ValueError as e:
#     print(f"Invalid RSS feed URL: {e}")