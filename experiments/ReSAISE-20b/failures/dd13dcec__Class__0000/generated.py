import re
from urllib.parse import urlparse, urlunparse

# Trusted RSS providers (add more as needed)
_TRUSTED_HOSTS = {
    "feeds.npr.org",
    "rss.cnn.com",
    "www.reddit.com",
    "news.ycombinator.com",
}

# Regular expression for private IP ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    ^(
        (10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or loopback range."""
    return bool(_PRIVATE_IP_RE.match(ip))


def _is_trusted_host(host: str) -> bool:
    """Check if the host is in the list of trusted providers."""
    # Normalise to lower case and strip trailing dot
    host = host.lower().rstrip(".")
    return any(host == trusted or host.endswith("." + trusted) for trusted in _TRUSTED_HOSTS)


def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate that a given RSS feed URL points to a trusted provider and does not
    expose internal or private networks.

    Parameters
    ----------
    feed_url : str
        The RSS feed URL to validate and sanitize.

    Returns
    -------
    str
        A sanitized, canonicalised URL that is guaranteed to be safe.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a private IP,
        or is not in the list of trusted providers.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    parsed = urlparse(feed_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject private or loopback IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private or loopback IP address")

    # Reject hostnames that resolve to private IPs (basic check)
    try:
        import socket

        resolved_ips = socket.gethostbyname_ex(parsed.hostname)[2]
    except Exception:
        raise ValueError("Unable to resolve hostname")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError("Hostname resolves to a private IP address")

    # Ensure host is trusted
    if not _is_trusted_host(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not a trusted provider")

    # Rebuild the URL to canonical form (no fragments, normalise query)
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            re.sub(r"/+$", "", parsed.path),  # strip trailing slashes
            parsed.params,
            parsed.query,
            "",
        )
    )

    return sanitized