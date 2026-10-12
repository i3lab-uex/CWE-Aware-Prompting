import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (hostnames or domain suffixes)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com/rss",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
    "rss.reuters.com",
    # add more trusted domains here
}

# Regex to detect private IP addresses (RFC 1918, RFC 1698, etc.)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}|
        0\.0\.0\.0|255\.255\.255\.255
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Determine if a host is a private IP address.
    Returns True for private IPs, False otherwise.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address, so we cannot say it's private.
        return False


def _is_trusted_host(host: str) -> bool:
    """
    Check if the host matches one of the trusted providers.
    Supports both exact matches and subdomain suffixes.
    """
    # Normalize host (remove trailing dot)
    host = host.rstrip(".").lower()

    if host in TRUSTED_PROVIDERS:
        return True

    # Check for suffix match (e.g., subdomain of a trusted domain)
    return any(host.endswith("." + provider) for provider in TRUSTED_PROVIDERS)


def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL to ensure it originates from a trusted provider.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL that needs validation.

    Returns
    -------
    str
        The sanitized feed URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted host,
        or attempts to access a private/internal network address.
    """
    if not rss_link:
        raise ValueError("RSS link cannot be empty.")

    parsed = urlparse(rss_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or host.")

    # Reject URLs that resolve to private IP addresses
    netloc = parsed.netloc.split(":")[0]  # strip port if present

    if _is_private_ip(netloc):
        raise ValueError("URL points to a private IP address.")

    # Reject URLs that point to localhost
    if netloc in ("localhost", "127.0.0.1"):
        raise ValueError("URL points to localhost.")

    # Ensure host is from a trusted provider
    if not _is_trusted_host(netloc):
        raise ValueError(f"Untrusted host: {netloc}")

    # Reconstruct the URL to ensure it's canonical
    sanitized = urlunparse(parsed._replace(path=parsed.path or "/", params="", query=""))
    return sanitized


# Example usage (for debugging only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost/feed",
        "https://example.com/feed",
    ]
    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" ->", clean_feed_link(url))
        except ValueError as e:
            print(f"  Error: {e}")