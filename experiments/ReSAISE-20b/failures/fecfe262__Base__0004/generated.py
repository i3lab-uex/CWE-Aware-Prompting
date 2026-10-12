import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved RSS providers (netlocs)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
    "news.google.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "rss2.feedly.com",
}

# Regular expression to detect IP addresses (IPv4 & IPv6)
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,7}:
            |
                (?:[0-9a-fA-F]{1,4}\:){1,6}:[0-9a-fA-F]{1,4}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}
            |
                (?:[0-9a-fA-F]{1,4}\:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}
            |
                [0-9a-fA-F]{1,4}\:(?::[0-9a-fA-F]{1,4}){1,6}
            |
                :(?::[0-9a-fA-F]{1,4}){1,7}
            |
                ::
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)

# Private IP ranges to block
PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # Loopback
    ipaddress.ip_network("::1/128"),     # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),   # Link-local
]


def _is_private_ip(host: str) -> bool:
    """
    Determine whether a host string is an IP address that falls within
    any of the private network ranges.
    """
    # Strip brackets for IPv6 literal addresses
    host_clean = host.strip("[]")
    try:
        ip_obj = ipaddress.ip_address(host_clean)
    except ValueError:
        return False
    for net in PRIVATE_RANGES:
        if ip_obj in net:
            return True
    return False


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_feed_url : str
        The raw URL supplied by an external component.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider, uses a disallowed scheme,
        or attempts to reach a private/internal network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url)

    # Enforce https or http
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    host = parsed.hostname.lower()

    # Disallow IP addresses (both IPv4 & IPv6)
    if re.match(IP_REGEX, host):
        raise ValueError("IP addresses are not allowed in RSS feed URLs")

    # Block private / loopback IP ranges
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private or loopback address")

    # Enforce trusted provider
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure no query params or fragments
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized