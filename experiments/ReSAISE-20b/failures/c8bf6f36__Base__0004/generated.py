import re
from urllib.parse import urlparse, unquote

# Trusted RSS providers – this list can be extended as needed.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.yahoo.com/rss",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                              # non-capturing group for the whole IP
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |
        192\.168\.\d{1,3}\.\d{1,3} |
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or loopback range."""
    return bool(PRIVATE_IP_RE.match(ip))

def validate_rss_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL points to a trusted provider and does not
    reference private or internal network addresses.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe to use.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved provider, is malformed,
        or attempts to resolve a private/internal address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalise hostname (case-insensitive, strip trailing dot)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    host = host.rstrip(".").lower()

    # Check that the hostname is in our trusted list
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname {host!r} is not in the list of trusted providers")

    # Additional safety: disallow IP addresses directly
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if _is_private_ip(host):
            raise ValueError(f"IP address {host!r} is private or internal")
        # Even if the IP is public, it should not be used directly
        raise ValueError(f"Direct IP addresses are not allowed: {host!r}")

    # Ensure the path is properly decoded and doesn't contain null bytes
    path = unquote(parsed.path)
    if "\0" in path:
        raise ValueError("Null byte detected in URL path")

    # Reconstruct the sanitized URL
    sanitized = parsed._replace(path=path, params="", query="", fragment="").geturl()
    return sanitized