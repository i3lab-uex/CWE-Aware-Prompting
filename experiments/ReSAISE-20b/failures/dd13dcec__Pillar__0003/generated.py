import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS feed domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regular expression for a valid hostname (simplified)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP address string is private or reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_reserved or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False


def _is_trusted_domain(host: str) -> bool:
    """Check if the host is in the list of trusted domains or a sub‑domain thereof."""
    # Ensure host ends with one of the trusted domains
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    feed_url : str
        The raw RSS feed URL supplied by a user.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL ready for fetching.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an untrusted domain,
        or attempts to resolve to a private/loopback IP address.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    # Parse the URL
    parsed = urlparse(feed_url)

    # Must use HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Validate host
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses directly
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        if _is_private_ip(host):
            raise ValueError("Access to private IP addresses is forbidden")
        # If it's a public IP, we still reject it unless it's mapped to a trusted domain
        raise ValueError("Direct IP addresses are not allowed")

    # Validate hostname format
    if not HOSTNAME_RE.match(host):
        raise ValueError("Invalid hostname in URL")

    # Ensure the host is trusted
    if not _is_trusted_domain(host.lower()):
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers")

    # Reconstruct a clean URL (strip fragments, preserve query)
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            "",  # fragment
        )
    )

    return sanitized