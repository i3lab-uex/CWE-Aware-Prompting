import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (domain names). Add or remove as needed.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression to detect IPv4 or IPv6 addresses in a host component.
_IP_RE = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )
    $
""", re.VERBOSE)

def _is_private_ip(host: str) -> bool:
    """
    Return True if host is a private IP address (IPv4 or IPv6).
    """
    try:
        # Strip brackets for IPv6 literal
        host_clean = host.strip("[]")
        ip_obj = ipaddress.ip_address(host_clean)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        return False

def validate_feed_source(feed_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL that needs validation.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to access
        an internal/private network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Reject empty netloc
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Disallow URLs with an IP address that is private or loopback
    if _IP_RE.match(parsed.netloc):
        if _is_private_ip(parsed.netloc):
            raise ValueError("URL points to a private or loopback IP address, which is disallowed.")
        # If it's a public IP we still reject it because we only trust domain names
        raise ValueError("URL uses a public IP address; only trusted domain names are allowed.")

    # Extract the host part (may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Case-insensitive comparison for trusted domains
    if host.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers.")

    # Reconstruct a sanitized URL (remove any query parameters or fragments)
    sanitized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return sanitized