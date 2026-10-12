import re
from urllib.parse import urlparse

# Define a list of trusted providers' domains (case‑insensitive)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "news.google.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private IP addresses and localhost
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (?:127\.0\.0\.1)|
        # IPv6 loopback
        (::1)
    )$
    """,
    re.VERBOSE,
)

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider
    and does not point to an internal or private network address.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private IP address or hostname,
        or does not belong to a trusted provider.
    """
    # Basic URL parsing
    try:
        parsed = urlparse(url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid URL format: {url}") from exc

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve hostname to IP if possible
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check for private IP addresses via regex on host (if numeric)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if PRIVATE_IP_RE.match(host):
            raise ValueError("URL points to a private IP address")

    # Ensure the hostname is in the list of trusted domains
    host_lower = host.lower()
    if not any(host_lower == domain or host_lower.endswith("." + domain)
               for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted provider: {host}")

    # All checks passed
    return url