import re
from urllib.parse import urlparse, unquote

# --------------------------------------------------------------------------- #
# Trusted RSS providers (add or remove as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogspot.com",
    "medium.com/feed",
    "wordpress.org/blogs.dir/1/rss.xml",
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
_IP_RE = re.compile(
    r"""
    ^(?:                           # start of string
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}   # IPv4
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})            # IPv4 last octet
        |                                         # or
        \[                                       # IPv6 start
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]                                       # IPv6 end
    )$
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_ip_address(host: str) -> bool:
    """Return True if host looks like an IP address."""
    return bool(_IP_RE.match(host))

def _is_localhost(host: str) -> bool:
    """Return True if host is a localhost reference."""
    return host.lower() in ("localhost", "127.0.0.1", "[::1]")

def _domain_allowed(host: str) -> bool:
    """Check if the host matches one of the trusted domains."""
    # Allow subdomains of the trusted list
    for domain in _TRUSTED_DOMAINS:
        if host.lower() == domain or host.lower().endswith("." + domain):
            return True
    return False

# --------------------------------------------------------------------------- #
def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL points to a trusted provider.

    Parameters
    ----------
    rss_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an IP address,
        references localhost, or does not belong to a trusted domain.
    """
    if not rss_address:
        raise ValueError("RSS address cannot be empty")

    # Parse the URL
    parsed = urlparse(rss_address.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {rss_address}")

    # Reject non-HTTP(S) schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject IP addresses and localhost
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("RSS URL must not use an IP address")
    if _is_localhost(host):
        raise ValueError("RSS URL must not reference localhost")

    # Ensure host is within the trusted list
    if not _domain_allowed(host):
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct a clean URL (remove fragments, normalize path)
    cleaned_path = re.sub(r"/+", "/", parsed.path)  # collapse duplicate slashes
    cleaned_query = parsed.query

    sanitized_url = f"{parsed.scheme}://{host}{cleaned_path}"
    if cleaned_query:
        sanitized_url += f"?{cleaned_query}"

    # Optionally, ensure the URL is percent‑encoded correctly
    sanitized_url = unquote(sanitized_url)

    return sanitized_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple tests
    test_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://feeds.feedburner.com/example/feed",
        "https://blogspot.com/yourfeed/rss.xml",
        "http://127.0.0.1/feed",          # should raise
        "https://evil.com/rss.xml",       # should raise
    ]

    for url in test_urls:
        try:
            print("Validating:", url)
            print("->", check_rss_address(url))
        except ValueError as exc:
            print(f"Rejected: {exc}")