import re
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Trusted RSS providers.  Add or remove domains as needed.
# Each entry may be a domain (e.g., "example.com") or a sub‑domain pattern
# that ends with the domain (e.g., "*.news.org").
_TRUSTED_DOMAINS = [
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reuters.com",
    "feed.theguardian.com",
]

# Regular expression to detect private IP ranges and localhost
_PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.0\.0\.1$)|
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$)|
    (^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$)|
    (^192\.168\.\d{1,3}\.\d{1,3}$)|
    (^169\.254\.\d{1,3}\.\d{1,3}$)
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is a private or loopback address."""
    return bool(_PRIVATE_IP_RE.match(ip))

def _is_trusted_domain(netloc: str) -> bool:
    """Check if the netloc matches one of the trusted domains."""
    # Normalize to lowercase
    host = netloc.lower()

    for pattern in _TRUSTED_DOMAINS:
        if pattern.startswith("*"):
            # e.g., "*.news.org" matches "sub.news.org"
            domain = pattern[2:]
            if host.endswith(domain) and len(host.split(".")) > domain.count(".") + 1:
                return True
        else:
            if host == pattern:
                return True
    return False

def check_rss_source(source_url: str) -> str:
    """
    Validate that a given RSS feed URL originates from a trusted provider
    and does not point to an internal or private network address.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP(S), if the host is private,
        or if the domain is not in the trusted list.
    """
    parsed = urlparse(source_url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError(f"URL points to a private IP: {parsed.hostname!r}")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted RSS source: {parsed.netloc!r}")

    # Re‑construct the URL to ensure it is normalized
    return parsed.geturl()