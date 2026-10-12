import re
from urllib.parse import urlparse, urlunparse

# List of trusted providers – add or modify as needed
TRUSTED_PROVIDERS = {
    "feeds.example.com",
    "news.google.com",
    "rss.nytimes.com",
    "medium.com/feed",
}

# Regular expression to detect private or loopback IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                              # start of group
        10(?:\.\d{1,3}){3}           |   # 10.0.0.0/8
        127(?:\.\d{1,3}){3}          |   # 127.0.0.0/8
        169\.254(?:\.\d{1,3}){2}     |   # 169.254.0.0/16
        172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2} |   # 172.16.0.0/12
        192\.168(?:\.\d{1,3}){2}     |   # 192.168.0.0/16
        100\.64(?:\.\d{1,3}){2}      |   # 100.64.0.0/10
        192\.0\.2(?:\.\d{1,3}){1}    |   # 192.0.2.0/24
        198\.51\.100(?:\.\d{1,3}){1} |   # 198.51.100.0/24
        203\.0\.113(?:\.\d{1,3}){1}      # 203.0.113.0/24
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_trusted_domain(domain: str) -> bool:
    """Check if the domain matches any trusted provider."""
    # Normalise subdomains: only exact match or end with a trusted suffix
    for provider in TRUSTED_PROVIDERS:
        if domain == provider or domain.endswith("." + provider):
            return True
    return False

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
        A canonicalised, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or targets a private network.
    """
    if not rss_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(rss_url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject URLs with missing netloc
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Normalise the netloc: strip port if present
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("Unable to parse hostname")

    # Reject private or loopback IP addresses
    if re.match(r"\d+\.\d+\.\d+\.\d+", host) and _is_private_ip(host):
        raise ValueError("URL points to a private or reserved IP address")

    # Ensure the host is in the trusted provider list
    if not _is_trusted_domain(host):
        raise ValueError(f"Untrusted provider: {host}")

    # Rebuild a canonical URL (drop userinfo, fragments, query parameters that are not relevant)
    cleaned = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return cleaned