import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully qualified domain names or domain suffixes that are trusted.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    # add more providers as needed
}

# Private IP ranges that must be blocked to prevent internal network access.
PRIVATE_RANGES = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv6Network("fc00::/7"),   # Unique local addresses
    ipaddress.IPv6Network("fe80::/10")   # Link-local addresses
]


def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address string falls within a private network range.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for net in PRIVATE_RANGES:
        if addr in net:
            return True
    return False


def _is_trusted_host(host: str) -> bool:
    """
    Verify that the host matches one of the trusted providers or their
    domain suffixes.
    """
    # Exact match
    if host in TRUSTED_PROVIDERS:
        return True

    # Domain suffix check (e.g., sub.example.com -> example.com)
    for provider in TRUSTED_PROVIDERS:
        if host.endswith("." + provider):
            return True

    return False


def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider and
    does not point to a private/internal network.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL suitable for fetching.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to access an
        internal network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{parsed.hostname}': {exc}")

    # Check that at least one resolved IP is not private
    for entry in addr_info:
        ip = entry[4][0]
        if not _is_private_ip(ip):
            break
    else:
        # All resolved IPs are private
        raise ValueError(f"Hostname '{parsed.hostname}' resolves to a private network address")

    # Verify host is in trusted list
    if not _is_trusted_host(parsed.hostname.lower()):
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the list of trusted providers")

    # Rebuild a sanitized URL (remove fragment, preserve query)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,
        ""   # fragment removed
    ))

    return sanitized