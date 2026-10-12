import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS feed providers (case‑insensitive)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.bbc.co.uk",
    "feeds.bbci.co.uk",
}

# Regular expression for a valid domain name (RFC 1035)
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$",
    re.IGNORECASE,
)


def _is_private_or_local(host: str) -> bool:
    """
    Return True if the host is an IP address or a hostname that resolves
    to a private, loopback, link‑local or reserved IP.
    """
    try:
        # Try interpreting the host as an IP address
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP address, assume it is a hostname
        return False

    # Check for private or non‑public IP ranges
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
    )


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
        A canonical, validated RSS feed URL that points to a trusted provider.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS,
        if it resolves to a private IP or local hostname,
        or if the host is not in the list of trusted providers.
    """
    if not feed_url:
        raise ValueError("Empty URL")

    parsed = urlparse(feed_url)

    # Enforce http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Reject URLs that resolve to private or local IPs
    if _is_private_or_local(host):
        raise ValueError("URL points to a private or local network address")

    # Normalize the host for comparison
    normalized_host = host.lower()

    if not DOMAIN_RE.match(normalized_host):
        raise ValueError(f"Invalid hostname: {host}")

    # Ensure the host is one of the trusted domains
    if not any(
        normalized_host == td or normalized_host.endswith("." + td)
        for td in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Untrusted provider: {host}")

    # Reconstruct the URL to remove fragments and query parameters
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            normalized_host,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized