import re
from urllib.parse import urlparse, urlunparse

# List of trusted provider hostnames.  Add or remove as needed.
TRUSTED_PROVIDERS = {
    "rss.example.com",
    "feeds.nytimes.com",
    "news.bbc.co.uk",
}

# Regular expression to detect numeric IP addresses (IPv4 or IPv6)
_IP_RE = re.compile(r"""
    ^(
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3} |
        # IPv6 (simple check)
        \[?[0-9a-fA-F:]+\]?
    )$
""", re.VERBOSE)

# Regular expression to reject private / loopback IP ranges
_PRIVATE_IP_RE = re.compile(r"""
    ^(
        # 10.0.0.0/8
        10\.
        |
        # 172.16.0.0/12
        172\.(1[6-9]|2\d|3[01])\.
        |
        # 192.168.0.0/16
        192\.168\.
        |
        # IPv6 loopback ::1
        \[?::1\]?
    )$
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if host is a numeric IP address."""
    return bool(_IP_RE.match(host))


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private or loopback IP address."""
    return bool(_PRIVATE_IP_RE.match(host))


def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, trusted RSS feed URL that can be safely fetched.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, contains a private IP address,
        or does not belong to a trusted provider.
    """
    if not rss_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(rss_url)

    # Enforce HTTPS for secure transport
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject numeric IP addresses or private ranges
    if _is_ip_address(host) and _is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP address")

    # Reject any hostname that is not in the trusted provider list
    if host.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Reconstruct the URL to ensure no extraneous fragments or queries
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         url = secure_feed_link("https://feeds.nytimes.com/nyt/rss/HomePage")
#         print("Sanitized URL:", url)
#     except ValueError as e:
#         print("Validation failed:", e)