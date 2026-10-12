import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Whitelisted RSS providers (case‑insensitive).  Add or remove entries as
# required for your deployment.
WHITELISTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "feeds.feedburner.com",
    "news.google.com",   # Google News feed
    "rss.reuters.com",
    "www.theguardian.com",
    "rss.msn.com",
    "news.yahoo.com",
}

# Regular expression to match common public DNS patterns
PUBLIC_DNS_PATTERN = re.compile(r"^(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$")

def _is_public_hostname(hostname: str) -> bool:
    """Return True if the hostname is a valid public domain name."""
    return bool(PUBLIC_DNS_PATTERN.match(hostname))

def _is_public_ip(address: str) -> bool:
    """Return True if the address is a public IP (IPv4 or IPv6)."""
    try:
        ip = ipaddress.ip_address(address)
        return not (ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast)
    except ValueError:
        return False

def _validate_hostname(hostname: str) -> None:
    """Validate that the hostname is either a public domain or a public IP."""
    if _is_public_hostname(hostname):
        return
    # If hostname looks like an IP address, validate it
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) or re.match(r"^[0-9a-fA-F:]+$", hostname):
        if not _is_public_ip(hostname):
            raise ValueError(f"Hostname {hostname!r} resolves to a private or reserved IP.")
        return
    raise ValueError(f"Hostname {hostname!r} is not a public domain or IP address.")

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_feed_url : str
        The raw URL of the RSS feed.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or points to a private network.
    """
    if not rss_feed_url:
        raise ValueError("Empty URL provided.")

    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme {parsed.scheme!r}. Only HTTP/HTTPS are allowed.")

    # Normalise the hostname to lowercase
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname.")

    # 1. Check against the whitelist
    if host not in WHITELISTED_PROVIDERS:
        raise ValueError(f"Hostname {host!r} is not in the whitelist of trusted providers.")

    # 2. Ensure hostname resolves to a public IP or is a valid public domain
    _validate_hostname(host)

    # Reconstruct the URL with cleaned components
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
# try:
#     print(filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
# except ValueError as e:
#     print(f"Invalid feed URL: {e}")