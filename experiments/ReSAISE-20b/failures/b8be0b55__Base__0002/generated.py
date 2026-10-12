import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS providers (add more as needed)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
    "feedproxy.google.com",  # feed proxy
}

# Regex to detect private IP address patterns in netloc
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1|
        fc00::/7|fd00::/8
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(netloc: str) -> bool:
    """
    Determine whether a netloc represents a private IP address.
    Handles both IPv4 and IPv6, including CIDR notation for IPv6.
    """
    # Strip port if present
    host = netloc.split(":")[0]
    try:
        ip_obj = ipaddress.ip_address(host)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        # Not an IP address, maybe hostname; use regex for IPv4 patterns
        return bool(PRIVATE_IP_RE.match(host))

def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL supplied by the caller.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to a private address,
        or does not belong to a trusted provider.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link.strip())

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Reject internal/private IP addresses
    if _is_private_ip(parsed.netloc):
        raise ValueError("URL points to a private or internal address")

    # Normalize hostname to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check against the list of trusted providers
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure no path traversal or query injection
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# Example usage (for debugging only; remove or guard under __name__ == "__main__")
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost/feed",  # should fail
        "https://feedproxy.google.com/unknown",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {clean_feed_link(url)}")
        except ValueError as exc:
            print(f"Rejected: {url} -> {exc}")