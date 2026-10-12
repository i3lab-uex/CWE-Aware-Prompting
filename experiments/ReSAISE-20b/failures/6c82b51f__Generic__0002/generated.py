import re
from urllib.parse import urlparse, urlunparse

# List of fully-qualified domain names that are considered trusted providers.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.yahoo.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    # Add more trusted providers here
}

# Regular expression to detect private IP address ranges.
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|127\.0\.0\.1)$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    return PRIVATE_IP_RE.match(ip) is not None

def _normalize_url(parsed: "ParseResult") -> str:
    """
    Reconstruct the URL with lowercase scheme and netloc,
    stripped trailing slashes, and encoded query parameters.
    """
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Ensure path does not end with a slash unless it's the root.
    path = parsed.path.rstrip("/") or "/"

    return urlunparse((scheme, netloc, path, "", parsed.query, ""))

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be validated.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or points to a restricted network.
    """
    if not rss_link:
        raise ValueError("The RSS link must be a non-empty string.")

    parsed = urlparse(rss_link)

    # Ensure scheme is HTTP or HTTPS.
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that use an IP address instead of a hostname.
    netloc = parsed.netloc.split(":")[0]  # drop optional port
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", netloc):
        if _is_private_ip(netloc):
            raise ValueError("URL points to a private IP address.")
        else:
            # Reject all bare IP addresses; only allow hostnames.
            raise ValueError("URL must use a hostname, not an IP address.")

    # Check if the hostname is in the trusted providers list.
    if netloc not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {netloc}")

    # Return a cleaned, canonical URL.
    return _normalize_url(parsed)