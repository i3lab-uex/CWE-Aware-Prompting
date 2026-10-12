import re
from urllib.parse import urlparse, urlunparse

# Whitelisted RSS providers (hostnames). Add or remove as needed.
_TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.yahoo.com",
    "www.reddit.com",
    "feeds.bbci.co.uk",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Regex to detect private IP ranges (RFC1918) and loopback
_PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                         # Loopback
    (^10\.)|                          # Private 10.0.0.0/8
    (^172\.(1[6-9]|2[0-9]|3[01])\. )| # Private 172.16.0.0/12
    (^192\.168\.)                     # Private 192.168.0.0/16
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private IP address."""
    try:
        # Resolve hostname to IP
        import socket

        ip = socket.gethostbyname(host)
    except Exception:
        return False  # If we cannot resolve, assume it's not private
    return bool(_PRIVATE_IP_RE.match(ip))


def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL is from a trusted provider and does not
    point to internal or private networks.

    Parameters:
        rss_address (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized and validated feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider or attempts
                    access to restricted internal networks.
    """
    if not isinstance(rss_address, str):
        raise ValueError("rss_address must be a string")

    parsed = urlparse(rss_address)

    # Validate scheme
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

    # Validate hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must have a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject hostnames not in the whitelist
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Rebuild the URL to ensure no path traversal or query manipulation
    sanitized = urlunparse(
        (
            parsed.scheme,
            host,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized