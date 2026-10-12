import re
from urllib.parse import urlparse, urlunparse

# List of trusted providers' hostnames (case‑insensitive)
_TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",  # example provider
}

# Regular expression to detect private IP ranges or localhost
_PRIVATE_IP_RE = re.compile(
    r"^(?:127\.0\.0\.1|"
    r"(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(?:192\.168\.\d{1,3}\.\d{1,3})|"
    r"::1)$",
    re.IGNORECASE
)

def _is_private_host(host: str) -> bool:
    """Return True if host is a private IP or localhost."""
    # If host is an IPv4/IPv6 address
    if _PRIVATE_IP_RE.match(host):
        return True

    # Resolve potential IPv4/IPv6 literals in brackets
    if host.startswith("[") and host.endswith("]"):
        addr = host[1:-1]
        if _PRIVATE_IP_RE.match(addr):
            return True

    # If host is a domain, we cannot resolve it here without DNS lookups.
    # For security, assume any non‑trusted domain is invalid.
    return False

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or points to a restricted network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize case for comparison
    host_lower = host.lower()

    # Reject private/internal hosts outright
    if _is_private_host(host_lower):
        raise ValueError(f"URL points to a restricted network: {host}")

    # Ensure the host is in the trusted list
    if host_lower not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {host}")

    # Reconstruct the URL to ensure no extra components are added
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host_lower,
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query as is
        ""   # fragment
    ))

    return sanitized

# Example usage (commented out)
# try:
#     url = check_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(url)
# except ValueError as e:
#     print(f"Invalid URL: {e}")