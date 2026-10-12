import re
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Configuration: trusted RSS providers
# ------------------------------------------------------------------
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
    "rss.slashdot.org",
    "www.bbc.co.uk",  # additional example
}

# ------------------------------------------------------------------
# Regular expressions for internal / private IP ranges
# ------------------------------------------------------------------
PRIVATE_IP_PATTERNS = [
    re.compile(r"^localhost$"),
    re.compile(r"^127\.0\.0\.1$"),
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$"),
]

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _is_private_host(host: str) -> bool:
    """
    Check if the host matches any known private/internal patterns.
    """
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True
    return False


def _is_trusted_provider(host: str) -> bool:
    """
    Determine if the host is in the list of approved RSS providers.
    """
    return host.lower() in TRUSTED_PROVIDERS


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider and
    does not point to internal or private networks.

    Parameters
    ----------
    rss_address : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is guaranteed to be from a
        trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted provider,
        or attempts to access a private/internal network.
    """
    if not rss_address:
        raise ValueError("RSS address must be a non‑empty string")

    # Parse the URL
    parsed = urlparse(rss_address)

    # Ensure scheme is present and safe
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # Reject internal / private hosts
    if _is_private_host(host):
        raise ValueError(f"URL points to a private or internal host: {host}")

    # Reject untrusted providers
    if not _is_trusted_provider(host):
        raise ValueError(f"Unapproved RSS provider: {host}")

    # Re‑construct the URL to avoid any path traversal or query injection
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     test_urls = [
#         "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
#         "http://localhost/feed",          # should fail
#         "https://evil.com/rss.xml",       # should fail
#     ]
#
#     for url in test_urls:
#         try:
#             print(f"Validating: {url}")
#             print(" ->", check_rss_address(url))
#         except ValueError as e:
#             print(f" -> Error: {e}")