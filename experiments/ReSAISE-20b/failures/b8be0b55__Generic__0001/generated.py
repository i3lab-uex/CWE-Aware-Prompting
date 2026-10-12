import re
from urllib.parse import urlparse, ParseResult

# Whitelisted providers – add or remove as needed
_WHITELISTED_DOMAINS = {
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.reuters.com",
    "rss.cnn.com",
}

# Regular expression to detect private IP addresses
_PRIVATE_IP_RE = re.compile(
    r"""
    (?:^|(?<=://))                 # Start or after scheme
    (?:
        10(?:\.\d{1,3}){3}         # 10.x.x.x
      | 172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}  # 172.16-31.x.x
      | 192\.168(?:\.\d{1,3}){2}   # 192.168.x.x
      | 127(?:\.\d{1,3}){3}        # localhost
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address.
    """
    return _PRIVATE_IP_RE.search(host) is not None

def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL by ensuring it originates from a trusted provider
    and does not point to any private/internal network addresses.

    Parameters:
        rss_link (str): The URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is not from a whitelisted domain,
                    points to a private IP, or fails basic validation.
    """
    if not rss_link:
        raise ValueError("Empty RSS link provided")

    parsed: ParseResult = urlparse(rss_link)

    # Basic URL validation
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal network address")

    # Reject hostnames that are not in the whitelist
    if host.lower() not in _WHITELISTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure consistency
    sanitized = parsed.geturl()
    return sanitized

# Example usage (commented out – remove for production)
# try:
#     print(clean_feed_link("https://feeds.bbci.co.uk/news/rss.xml"))
# except ValueError as exc:
#     print(f"Invalid feed: {exc}")