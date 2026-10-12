import re
from urllib.parse import urlparse, urlunparse, quote
import ipaddress

# List of trusted providers (example domains)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regular expression for a valid host (allows subdomains)
HOST_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

def _is_private_ip(host: str) -> bool:
    """
    Resolve a hostname to an IP address and check if it is private.
    Returns True for private or link‑local addresses.
    """
    try:
        # Try to interpret as an IP address directly
        ip = ipaddress.ip_address(host)
    except ValueError:
        # If not an IP, perform a simple lookup using the socket module
        import socket
        try:
            addr = socket.gethostbyname(host)
            ip = ipaddress.ip_address(addr)
        except Exception:
            # If resolution fails, treat as non‑private (fallback)
            return False
    return ip.is_private or ip.is_loopback or ip.is_link_local

def _normalize_url(parsed: urlparse) -> str:
    """
    Reconstruct a sanitized URL:
      * Lowercase scheme and host
      * Ensure path is percent‑encoded
    """
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = quote(parsed.path, safe="/")
    params = parsed.params
    query = parsed.query
    fragment = ""  # discard fragments
    return urlunparse((scheme, netloc, path, params, query, fragment))

def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The raw RSS feed URL supplied by the caller.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL ready for fetching.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS/HTTP,
        does not belong to a trusted provider, or
        resolves to an internal network address.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address.strip())

    # Basic scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use HTTP or HTTPS scheme")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Validate host format
    if not HOST_RE.match(parsed.hostname):
        raise ValueError("Hostname is not a valid domain")

    # Ensure the host is in the trusted list
    if parsed.hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError("Hostname is not a trusted provider")

    # Prevent internal network access
    if _is_private_ip(parsed.hostname):
        raise ValueError("Hostname resolves to a private or loopback address")

    # Sanitize the URL (percent‑encode path, lower case scheme/netloc)
    return _normalize_url(parsed)

# Example usage (uncomment to test):
# try:
#     url = validate_feed_source("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print("Validated URL:", url)
# except ValueError as e:
#     print("Validation failed:", e)