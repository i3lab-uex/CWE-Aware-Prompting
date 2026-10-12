import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (hostnames only)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "feeds.reuters.com",
    "rss.cnn.com",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address is in a private, loopback,
    link-local or reserved range.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If IP parsing fails, treat as non-private (allow the check to fail later)
        return False

def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers
    and ensure it does not resolve to a private IP address.

    Parameters:
        feed_address (str): The RSS feed URL to validate.

    Returns:
        str: The original, sanitized URL if it passes validation.

    Raises:
        ValueError: If the URL is not from a trusted provider,
                    uses an unsupported scheme, or resolves
                    to a restricted network address.
    """
    # Parse the URL
    parsed = urlparse(feed_address)

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname and port
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Remove port for provider comparison
    netloc = host

    if netloc not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{netloc}' is not a trusted provider")

    # Resolve hostname to IP addresses and ensure none are private
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP address {ip}")

    # Reconstruct a sanitized URL (remove fragments, ensure path)
    sanitized = parsed._replace(fragment="")  # drop fragment
    return urlunparse(sanitized)

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml?param=value#section",
        "https://malicious.example.com/feed",
    ]
    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_feed_source(url)
            print(f"  --> Validated URL: {result}")
        except ValueError as e:
            print(f"  !! Validation error: {e}")