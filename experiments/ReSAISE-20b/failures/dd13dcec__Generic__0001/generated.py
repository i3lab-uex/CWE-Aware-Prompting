import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted RSS feed providers.  The list can be extended as needed.
TRUSTED_DOMAINS = {
    # News outlets
    "nytimes.com",
    "bbc.co.uk",
    "cnn.com",
    # Feed providers
    "feeds.feedburner.com",
    "rsshub.app",
    # Blogs / personal sites
    "wordpress.com",
}

# Allow subdomains of the trusted domains (e.g. news.bbc.co.uk)
ALLOW_SUBDOMAINS = True

# Regular expression to detect private or reserved IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|^169\.254\.)   # IPv4
    |(^::1$)                                                             # IPv6 loopback
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_private_ip(hostname: str) -> bool:
    """
    Determine whether the hostname resolves to a private IP address.
    This function only checks literal IP addresses; it does not perform DNS resolution.
    """
    try:
        ipaddress.ip_address(hostname)
        return hostname in ("127.0.0.1", "::1")
    except ValueError:
        # Not a literal IP address
        return False


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check if the hostname is in the trusted domain list.
    """
    # Normalize to lowercase
    host = hostname.lower()
    if ALLOW_SUBDOMAINS:
        for domain in TRUSTED_DOMAINS:
            if host == domain or host.endswith("." + domain):
                return True
    else:
        return host in TRUSTED_DOMAINS
    return False


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw RSS feed URL provided by a user.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private or untrusted domain, or otherwise
        poses a security risk.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # 1. Scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # 2. Host presence
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname

    # 3. Reject literal private IP addresses
    if PRIVATE_IP_REGEX.match(host) or _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # 4. Verify trusted domain
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not trusted")

    # 5. Normalize: remove fragment, default port for http/https
    netloc = host
    if parsed.port:
        # Only keep port if it's non-standard (80 for http, 443 for https)
        default_port = 80 if parsed.scheme == "http" else 443
        if parsed.port != default_port:
            netloc = f"{host}:{parsed.port}"
    sanitized_parts = (
        parsed.scheme,
        netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        "",  # fragment
    )
    sanitized_url = urlunparse(sanitized_parts)

    return sanitized_url


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://feeds.feedburner.com/example/rss",
        "http://192.168.1.10/feed",  # should fail
        "https://malicious.com/rss",
        "ftp://example.com/feed",    # should fail
    ]

    for url in test_urls:
        try:
            print(f"Original: {url}")
            print(f"Sanitized: {sanitize_feed_url(url)}\n")
        except ValueError as e:
            print(f"Rejected: {e}\n")