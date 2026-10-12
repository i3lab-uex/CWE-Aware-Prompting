import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# Configuration: trusted providers and restricted IP ranges
# ------------------------------------------------------------------
TRUSTED_PROVIDERS = {
    "news.ycombinator.com",
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogspot.com",
}

# Restricted IP ranges (private, local, loopback)
RESTRICTED_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _is_ip_restricted(host: str) -> bool:
    """
    Return True if the host resolves to an IP address that falls into a
    restricted network range.  We only perform the check if the host is an IP.
    """
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP address, skip check
        return False

    for net in RESTRICTED_IP_RANGES:
        if ip in net:
            return True
    return False


def _is_trusted_provider(host: str) -> bool:
    """
    Verify that the host ends with one of the trusted provider domains.
    Subdomains are allowed as long as they match a trusted suffix.
    """
    host = host.lower()
    return any(host == provider or host.endswith("." + provider) for provider in TRUSTED_PROVIDERS)


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL supplied by a user.

    Returns
    -------
    str
        A sanitized, absolute RSS feed URL that is safe to fetch.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a non‑trusted provider,
        or attempts to resolve to an internal network address.
    """
    # Basic syntax validation
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    parsed = urlparse(rss_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Remove default ports to avoid false positives
    netloc = parsed.netloc.split("@")[-1]  # strip username if present
    host, _, port = netloc.partition(":")
    if port:
        try:
            int(port)  # ensure it's numeric
        except ValueError:
            raise ValueError("Port must be numeric")

    # 1. Check for restricted IP addresses
    if _is_ip_restricted(host):
        raise ValueError("URL resolves to a restricted IP address")

    # 2. Check that the host is from a trusted provider
    if not _is_trusted_provider(host):
        raise ValueError(f"Host '{host}' is not from a trusted provider")

    # 3. Re‑construct the URL to ensure no hidden fragments/parameters
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "", "", "", "")
    )

    return sanitized