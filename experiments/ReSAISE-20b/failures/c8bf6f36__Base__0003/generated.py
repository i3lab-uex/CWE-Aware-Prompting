import re
from urllib.parse import urlparse, urlunparse

# List of trusted RSS providers. Add or remove domains as needed.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "news.google.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private IP addresses.
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 loopback
        (::1)
    )
    """,
    re.VERBOSE,
)

# Regular expression to detect any IP address in the hostname.
_IP_ADDRESS_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        \d{1,3}(?:\.\d{1,3}){3}|
        # IPv6 (simplified)
        \[[0-9a-fA-F:]+\]
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if host resolves to a private IP address or localhost."""
    return bool(_PRIVATE_IP_REGEX.match(host))


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(_IP_ADDRESS_REGEX.match(host))


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the given RSS link points to a trusted provider and
    does not target an internal network.

    Parameters:
        rss_link (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized, fully-qualified URL that is safe to fetch.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP,
                    points to a private IP, or is from an untrusted domain.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Host validation
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses or localhost
    if _is_ip_address(host):
        raise ValueError("URL must not contain an IP address")
    if _is_private_ip(host):
        raise ValueError("URL must not target a private or local network")

    # Ensure domain is in the whitelist
    if host.lower() not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved RSS provider")

    # Reconstruct the URL to ensure it is canonical
    sanitized = urlunparse(
        (
            parsed.scheme,
            host.lower(),
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query string if any
            "",  # fragment
        )
    )

    return sanitized