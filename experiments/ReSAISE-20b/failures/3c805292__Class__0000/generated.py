import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# List of fully qualified domain names (FQDNs) that are considered trusted.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",          # example provider
    "feed.polygon.com",
}

# Regular expression to detect private IP addresses (RFC1918 and loopback).
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        # 172.16.0.0 – 172.31.255.255
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        # 192.168.0.0 – 192.168.255.255
        192\.168\.\d{1,3}\.\d{1,3}|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    The function performs a simple regex check for IPv4 literals
    and resolves DNS names to IP addresses if necessary.
    """
    # Quick check for obvious private IPv4 literals
    if PRIVATE_IP_RE.match(host):
        return True

    # Resolve the host to IPs and check each one
    try:
        import socket

        for ip in socket.gethostbyname_ex(host)[2]:
            if ipaddress.ip_address(ip).is_private:
                return True
    except Exception:  # pragma: no cover
        # Any resolution failure is treated as unsafe; better safe than sorry.
        return True

    return False


def validate_feed_source(feed_address: str) -> str:
    """
    Validate that the provided RSS feed URL is from a trusted provider
    and does not point to any internal or private network.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized and canonicalized URL that has been validated.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, uses an unsupported scheme,
        or attempts to connect to a private/internal network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Only allow http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP(S) are allowed.")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Normalize the netloc (lowercase)
    host = parsed.netloc.split(":")[0].lower()

    # Check for private IPs or internal networks
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal network address")

    # Verify the host is in the trusted providers list
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Rebuild the URL to remove any fragment or query parameters that might
    # influence downstream processing.  We keep the path, scheme, and netloc.
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path or "/",
        params="",
        query="",
        fragment="",
    )
    return urlunparse(sanitized)