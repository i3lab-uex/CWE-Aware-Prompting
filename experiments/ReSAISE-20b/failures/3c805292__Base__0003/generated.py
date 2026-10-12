import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully-qualified domain names (FQDNs) that are considered trusted.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "api.theguardian.com",
    # Add more trusted providers here
}

# Regular expression for a valid URL scheme (http or https)
_SCHEME_RE = re.compile(r"^(?:https?://)", re.IGNORECASE)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is in a private or non-routable range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local
    except ValueError:
        # Not an IP address, treat as not private
        return False

def _is_trusted_netloc(netloc: str) -> bool:
    """
    Determine whether the netloc (host[:port]) is part of a trusted provider.
    The host portion is matched case‑insensitively against TRUSTED_PROVIDERS.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    return host in TRUSTED_PROVIDERS

def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL against a list of trusted providers and
    ensure it does not point to private or internal networks.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely fetched.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑trusted provider, or attempts to resolve
        a private IP address.
    """
    if not feed_address:
        raise ValueError("Feed URL must be non‑empty")

    # Ensure the scheme is http or https
    if not _SCHEME_RE.match(feed_address):
        raise ValueError("Only http and https schemes are allowed")

    parsed = urlparse(feed_address)

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IP addresses
    try:
        # Resolve the host; if it resolves to an IP, check for private ranges
        ip_list = []
        import socket
        try:
            # Resolve all addresses for the host (IPv4 and IPv6)
            ip_list = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
        except socket.gaierror:
            # If DNS resolution fails, let the caller handle it later
            pass

        for addr in ip_list:
            family, _, _, _, sockaddr = addr
            if family == socket.AF_INET:  # IPv4
                ip_str = sockaddr[0]
            elif family == socket.AF_INET6:  # IPv6
                ip_str = sockaddr[0]
            else:
                continue

            if _is_private_ip(ip_str):
                raise ValueError(f"URL resolves to a private IP address: {ip_str}")

    except Exception as exc:
        # If any exception occurs during resolution, treat it as unsafe
        raise ValueError(f"Failed to validate host: {exc}") from exc

    # Verify the host is in the trusted list
    if not _is_trusted_netloc(parsed.netloc):
        raise ValueError(f"Untrusted provider: {parsed.hostname}")

    # Reconstruct the URL to ensure it is canonical
    sanitized = urlunparse(parsed._replace(fragment=""))  # strip fragment
    return sanitized

# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://malicious.example.com/feed",
        "http://localhost:8000/feed.xml",
    ]
    for url in test_urls:
        try:
            print("Validating:", url)
            print("  ->", validate_feed_source(url))
        except ValueError as e:
            print("  !", e)