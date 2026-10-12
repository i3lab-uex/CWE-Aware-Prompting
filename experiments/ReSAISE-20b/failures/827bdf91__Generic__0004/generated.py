import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully-qualified domain names (FQDNs) that are allowed to provide RSS feeds.
TRUSTED_PROVIDERS = {
    "rss.example.com",
    "feeds.nytimes.com",
    "news.bbc.co.uk",
}

# Regular expression to detect private IP addresses or localhost.
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(?:192\.168\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    """
    try:
        # Resolve hostname to IP addresses
        for addr in ipaddress.ip_address(host).exploded.split(','):
            if PRIVATE_IP_RE.match(addr):
                return True
    except ValueError:
        # If host is not a valid IP address, assume it's a hostname.
        return False
    return False

def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL provided by the user.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or resolves to a private IP address.
    """
    if not rss_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(rss_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize hostname (lowercase, strip trailing dots)
    host = parsed.hostname.lower().rstrip(".") if parsed.hostname else ""

    # Check against the list of trusted providers
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host}")

    # Prevent internal network access by rejecting private IPs
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # Reconstruct the URL without any query or fragment for safety
    safe_url = urlunparse(
        (
            parsed.scheme,
            host,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        print(secure_feed_link("https://rss.example.com/latest.xml"))
    except ValueError as exc:
        print(f"Invalid feed URL: {exc}")