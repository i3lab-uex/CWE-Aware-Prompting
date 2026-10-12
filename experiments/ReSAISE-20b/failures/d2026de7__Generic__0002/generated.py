import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A whitelist of trusted RSS feed hosts.
_TRUSTED_HOSTS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "news.google.com",
    "rss.cnn.com",
    # add more trusted providers as needed
}

# Regular expression to detect potential IP addresses in hostnames.
_IP_PATTERN = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")

def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private IP address."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private
    except ValueError:
        # Not a numeric IP, assume hostname.
        return False

def _is_trusted_host(host: str) -> bool:
    """Check if the host is in the trusted whitelist."""
    # Strip trailing dot (FQDN) and compare case-insensitively.
    host = host.rstrip(".").lower()
    return host in _TRUSTED_HOSTS

def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL points only to trusted providers.

    Parameters
    ----------
    rss_address : str
        The URL of the RSS feed being validated.

    Returns
    -------
    str
        A sanitized, verified URL limited to trusted providers.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or attempts to access
        restricted internal networks.
    """
    if not rss_address:
        raise ValueError("RSS address must be a non-empty string")

    parsed = urlparse(rss_address)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IP addresses
    if _IP_PATTERN.match(host) and _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject URLs that are not in the trusted whitelist
    if not _is_trusted_host(host):
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure it is in a canonical form
    sanitized = urlunparse((
        parsed.scheme,
        host.lower(),
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return sanitized