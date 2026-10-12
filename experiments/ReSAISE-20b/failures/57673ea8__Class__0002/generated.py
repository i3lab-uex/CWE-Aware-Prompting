import ipaddress
from urllib.parse import urlparse

# A small whitelist of trusted RSS feed providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Private IP ranges (RFC 1918, loopback, link-local, etc.)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fe80::/10"),
]

def _is_private_ip(host: str) -> bool:
    """
    Determine whether the given host resolves to a private IP address.
    """
    try:
        # Resolve hostname to all associated IP addresses
        for ip_str in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP):
            ip = ipaddress.ip_address(ip_str[4][0])
            for network in PRIVATE_IP_RANGES:
                if ip in network:
                    return True
    except Exception:
        # If resolution fails we err on the side of caution and treat it as private
        return True
    return False

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider and
    does not point to an internal network.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated, canonical URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted provider,
        or resolves to a private IP address.
    """
    # Parse the URL and ensure it uses HTTP/HTTPS
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Check hostname against the trusted provider list
    if parsed.hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not on the trusted list")

    # Detect internal IP addresses (CWE‑441 concern)
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private IP address")

    # Reconstruct the URL to ensure consistent formatting
    canonical_url = parsed.geturl()
    return canonical_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://localhost/feed",  # should fail
    ]
    for u in test_urls:
        try:
            print("Validating:", u)
            print("Result:", validate_feed_url(u))
        except ValueError as e:
            print("Validation error:", e)