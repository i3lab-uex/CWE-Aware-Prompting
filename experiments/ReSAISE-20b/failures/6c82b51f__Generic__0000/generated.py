import re
from urllib.parse import urlparse, urlunparse

# List of trusted provider domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com/rss",
    "rss.cnn.com",
    # add more trusted domains here
}

# Regular expression to detect private IP addresses or localhost
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        10(?:\.\d{1,3}){3}|
        172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|
        192\.168(?:\.\d{1,3}){2}|
        127(?:\.\d{1,3}){3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private IP address or localhost."""
    try:
        # Resolve host to an IP (IPv4 only for simplicity)
        import socket
        ip = socket.gethostbyname(host)
    except Exception:
        # If resolution fails, assume it's not a private IP
        return False

    return bool(_PRIVATE_IP_RE.match(ip))

def _is_trusted_domain(host: str) -> bool:
    """Return True if the host ends with one of the trusted domains."""
    # Normalize to lowercase
    host = host.lower()
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑trusted domain or attempts to reach
        a private/internal network address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    # Parse the URL
    parsed = urlparse(rss_link.strip())

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP(S) URLs are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    # Reject URLs with credentials in the netloc
    if parsed.username or parsed.password:
        raise ValueError("Credentials are not allowed in the URL")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host):
        raise ValueError("URL points to a private or localhost address")

    # Ensure host is from the trusted domain list
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers")

    # Reconstruct a clean URL without userinfo or fragments
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # no fragment
    ))

    return cleaned

# Example usage (commented out):
# try:
#     safe_url = check_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Safe URL: {safe_url}")
# except ValueError as e:
#     print(f"Invalid RSS feed URL: {e}")