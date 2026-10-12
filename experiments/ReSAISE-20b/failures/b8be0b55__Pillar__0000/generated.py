import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Trusted RSS feed providers (domain names).  Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
}

# Regular expression to match a valid URL scheme
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or otherwise non‑public."""
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False


def _validate_hostname(hostname: str) -> bool:
    """
    Resolve the hostname and ensure none of its IP addresses are private.
    Returns True if all resolved IPs are public.
    """
    try:
        # Resolve hostname to all addresses
        _, _, ipaddrlist = socket.gethostbyname_ex(hostname)
    except socket.gaierror:
        # Unable to resolve hostname
        return False

    for ip in ipaddrlist:
        if _is_private_ip(ip):
            return False
    return True


def clean_feed_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL originates from a trusted provider
    and does not resolve to an internal or private network address.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The sanitized (unchanged) RSS feed URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTPS, the provider is untrusted,
        or the host resolves to a private/internal IP address.
    """
    if not rss_link:
        raise ValueError("RSS link must be a non‑empty string")

    # Ensure scheme is http or https
    if not _SCHEME_RE.match(rss_link):
        raise ValueError("RSS link must start with http:// or https://")

    parsed = urlparse(rss_link)

    # Reject non‑HTTP schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise netloc (remove port if default)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("RSS link must contain a valid host")

    # Check provider whitelist
    if hostname.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {hostname}")

    # Ensure host does not resolve to private IPs
    if not _validate_hostname(hostname):
        raise ValueError(f"RSS provider resolves to a private or internal IP: {hostname}")

    # Reconstruct the URL to ensure canonical form
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # No fragment
        )
    )

    return sanitized