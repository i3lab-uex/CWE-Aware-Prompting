import re
from urllib.parse import urlparse, urlunparse

# A list of approved RSS providers.  Add or remove entries as needed.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression to match private or loopback IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the supplied IP string is a private or loopback address."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_trusted_host(host: str) -> bool:
    """Check if the host is in our whitelist or is a non‑private domain name."""
    # Resolve IP addresses if the host looks like an IP.
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        return not _is_private_ip(host)

    # Domain names: allow only those explicitly listed.
    host_lower = host.lower()
    return any(host_lower == t or host_lower.endswith("." + t) for t in TRUSTED_DOMAINS)

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the given RSS feed URL points to a trusted provider.

    Parameters
    ----------
    rss_feed_url : str
        The URL of the RSS feed being validated.

    Returns
    -------
    str
        The same URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or attempts to access a restricted network.
    """
    if not rss_feed_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(rss_feed_url)

    # Basic sanity checks
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Block private IPs or loopback addresses
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) and _is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP address")

    # Ensure the host is on our whitelist
    if not _is_trusted_host(host):
        raise ValueError(f"Host '{host}' is not an approved RSS provider")

    # Re‑construct the URL to normalise it (e.g., remove fragments)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))
    return sanitized

# Example usage (commented out to avoid accidental execution)
# try:
#     url = filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Validated URL: {url}")
# except ValueError as e:
#     print(f"Validation error: {e}")