import re
from urllib.parse import urlparse, urlunparse

# List of trusted providers (domain names). Extend as needed.
TRUSTED_PROVIDERS = {
    "feeds.reuters.com",
    "rss.nytimes.com",
    "news.google.com",
    "feeds.bbci.co.uk",
    "rss.cnn.com",
    "news.ycombinator.com",
}

# Regex to detect private IP addresses (RFC 1918, RFC 1698, RFC 5735)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                                 # start group for IP patterns
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |    # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3} |    # 192.168.0.0/16
        169\.254\.\d{1,3}\.\d{1,3} |    # 169.254.0.0/16 (link-local)
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}   # 127.0.0.0/8 (loopback)
    )
    $
    """,
    re.VERBOSE,
)

def is_private_ip(host: str) -> bool:
    """
    Check if a host string is an IP address in a private or reserved range.
    """
    try:
        # Attempt to interpret host as an IP address
        import ipaddress

        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address; fallback to regex for known private patterns
        return bool(PRIVATE_IP_REGEX.match(host))


def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to be validated.

    Returns
    -------
    str
        A sanitized, secure RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or targets a private network.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    parsed = urlparse(rss_url)

    # Enforce HTTPS or HTTP scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Split hostname and port
    host = parsed.hostname or ""
    port = parsed.port

    # Reject private IP addresses or loopback
    if is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP address")

    # Reject hosts that are not in the trusted provider list
    if host.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Reconstruct the URL to ensure it has no path traversal or fragments
    safe_path = parsed.path if parsed.path else "/"
    sanitized_url = urlunparse(
        (
            parsed.scheme,
            f"{host}:{port}" if port else host,
            safe_path.rstrip("/"),
            "",  # params
            parsed.query,  # keep query parameters if any
            "",  # fragment
        )
    )

    return sanitized_url