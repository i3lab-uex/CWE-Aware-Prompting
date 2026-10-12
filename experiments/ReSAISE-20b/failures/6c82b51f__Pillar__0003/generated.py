import re
from urllib.parse import urlparse, urlunparse

# List of trusted providers (domain names)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "www.reddit.com",
    "blogspot.com",
}

# Regular expression to detect private or reserved IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:  # start of IP alternatives
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # 10.0.0.0 – 10.255.255.255
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0 – 172.31.255.255
        192\.168\.\d{1,3}\.\d{1,3} |          # 192.168.0.0 – 192.168.255.255
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |       # 127.0.0.0 – 127.255.255.255
        169\.254\.\d{1,3}\.\d{1,3} |          # Link-local 169.254.0.0 – 169.254.255.255
        192\.0\.2\.\d{1,3} |                  # TEST-NET-1
        198\.51\.100\.\d{1,3} |                # TEST-NET-2
        203\.0\.113\.\d{1,3}                   # TEST-NET-3
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    return bool(PRIVATE_IP_RE.match(ip))

def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The sanitized, validated URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, points to an internal network,
        or fails basic validation checks.
    """
    if not isinstance(rss_link, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(rss_link)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Ensure a host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses directly (public or private)
    host = parsed.hostname.lower()
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if _is_private_ip(host) or not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
            raise ValueError("Direct IP addresses are not allowed")
        # Reject all public IPs to avoid DNS rebinding attacks
        raise ValueError("Direct IP addresses are not allowed")

    # Reject any subdomains that are not in the trusted list
    if host not in TRUSTED_DOMAINS:
        # Allow subdomains of trusted domains (e.g., foo.rss.nytimes.com)
        if not any(host.endswith(f".{t}") for t in TRUSTED_DOMAINS):
            raise ValueError("Hostname not on the trusted provider list")

    # Reconstruct a canonical URL (remove fragment and query for safety)
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized