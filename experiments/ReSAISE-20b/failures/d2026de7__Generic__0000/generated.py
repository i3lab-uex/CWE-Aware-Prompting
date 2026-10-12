import re
from urllib.parse import urlparse, urlunparse


# List of approved RSS providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
    # Add more trusted domains here
}

# Regular expression to detect internal IP addresses (RFC1918 ranges)
INTERNAL_IP_RE = re.compile(
    r"^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3})$"
)


def _is_internal_ip(host: str) -> bool:
    """Check if the host is an internal IP address."""
    try:
        # Simple numeric check; in production use ipaddress module
        return INTERNAL_IP_RE.match(host) is not None
    except Exception:
        return False


def check_rss_address(rss_address: str) -> str:
    """
    Validate that the given RSS feed URL belongs to a trusted provider and
    does not point to an internal network.

    Parameters:
        rss_address (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized, fully-qualified URL that is guaranteed to be from
             a trusted provider.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a non-trusted domain, or attempts to access
                    internal networks.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize host (case-insensitive)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Reject internal IPs or localhost
    if _is_internal_ip(hostname) or hostname in ("localhost", "127.0.0.1"):
        raise ValueError("Access to internal network addresses is forbidden")

    # Check against trusted domains (case-insensitive)
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {hostname}")

    # Reconstruct the URL to ensure no additional query/path manipulation
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized


# Example usage (uncomment to test):
# try:
#     url = check_rss_address("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation failed: {e}")