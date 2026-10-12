import re
from urllib.parse import urlparse, urlunparse

# List of approved RSS providers (domains only)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.arstechnica.com",
}

# Regex for private IP ranges (RFC1918 and loopback)
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                               # IP address in dotted decimal
        (?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (?:(?:172\.)(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (?:(?:192\.168)\.\d{1,3}\.\d{1,3})|
        (?:169\.254\.\d{1,3}\.\d{1,3})
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if the host is a private IP address."""
    # Directly check numeric IP
    try:
        parts = [int(part) for part in host.split(".")]
        if len(parts) != 4:
            return False
        ip = ".".join(str(p) for p in parts)
        return bool(PRIVATE_IP_RE.match(ip))
    except ValueError:
        # Not a numeric IP; assume not private
        return False


def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_address : str
        The URL to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or attempts to reach a private network.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("RSS address must use http or https scheme")

    # Resolve hostname (may be IP)
    host = parsed.hostname
    if not host:
        raise ValueError("RSS address must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("RSS address points to a private network")

    # Reject domains not in the trusted list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(
        (
            parsed.scheme,
            host.lower(),
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query string if present
            "",  # fragment
        )
    )

    return sanitized