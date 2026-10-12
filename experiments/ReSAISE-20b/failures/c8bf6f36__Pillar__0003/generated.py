import re
from urllib.parse import urlparse, urlunparse

# A small list of approved RSS providers.  Add more trusted domains as needed.
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to detect private IP ranges and localhost
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    # 10.0.0.0 – 10.255.255.255
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    # 172.16.0.0 – 172.31.255.255
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|"
    # 192.168.0.0 – 192.168.255.255
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|"
    # 127.0.0.0 – 127.255.255.255
    r"127\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    # ::1 (IPv6 loopback)
    r"::1"
    r")$",
    re.IGNORECASE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private IP or localhost."""
    # Try numeric IPv4
    parts = host.split(".")
    if len(parts) == 4 and all(part.isdigit() for part in parts):
        return PRIVATE_IP_RE.match(host) is not None
    # IPv6 or hostname – we only check for localhost names here
    return host.lower() in {"localhost", "127.0.0.1"}


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the provided RSS link comes from a trusted provider.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized and normalized URL that is guaranteed to point to an approved provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private IP or localhost, or does not belong to an approved provider.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Enforce https or http
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject empty netloc (e.g., relative URLs)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Reject private IPs or localhost
    host = parsed.hostname
    if host is None:
        raise ValueError("URL does not contain a valid hostname")
    if _is_private_ip(host):
        raise ValueError("URL points to a private or local network address")

    # Normalize host to lower case for comparison
    host_lower = host.lower()

    if host_lower not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved RSS provider")

    # Reconstruct a clean URL (removes fragments, unnecessary query params)
    cleaned = urlunparse((
        parsed.scheme,
        host_lower,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return cleaned


# Example usage (commented out; remove for production)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://localhost/feed.xml",
        "ftp://example.com/feed.xml",
        "http://192.168.1.10/rss.xml",
    ]

    for url in test_urls:
        try:
            print(validate_rss_link(url))
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")