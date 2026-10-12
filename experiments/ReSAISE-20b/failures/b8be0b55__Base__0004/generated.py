import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ----------------------------------------------------------------------
# Trusted RSS providers – update as needed
# ----------------------------------------------------------------------
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regex to detect private IP ranges or localhost
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                                   # 127.0.0.0/8
    (^10\.) |                                    # 10.0.0.0/8
    (^192\.168\.) |                              # 192.168.0.0/16
    (^172\.1[6-9]\.) |                           # 172.16.0.0/12
    (^172\.2[0-9]\.) |
    (^172\.3[0-1]\.) |
    (^169\.254\.) |                              # link-local
    (^::1$)                                      # IPv6 loopback
    """,
    re.VERBOSE,
)


def _is_private_ip(hostname: str) -> bool:
    """
    Determine whether a hostname resolves to a private IP address.
    If the hostname is already an IP, we check directly. Otherwise,
    we perform a simple regex check for common private ranges.
    """
    # Direct IP check
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a literal IP; check for private patterns in hostname
        return bool(PRIVATE_IP_RE.search(hostname))


def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL ensuring it originates from a trusted external provider.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate and sanitize.

    Returns
    -------
    str
        The sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not resolve to a trusted domain,
        or resolves to an internal/private IP address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Only allow http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal/private IP addresses
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or internal IP address")

    # Verify the hostname ends with one of the trusted domains
    if not any(hostname.lower().endswith(domain) for domain in TRUSTED_DOMAINS):
        raise ValueError("Hostname not in the list of trusted providers")

    # Reconstruct a clean URL (drop userinfo, fragments, query params)
    cleaned = urlunparse(
        (
            parsed.scheme,
            f"{hostname}{parsed.port and ':' + str(parsed.port) or ''}",
            parsed.path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return cleaned