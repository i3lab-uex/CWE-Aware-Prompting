import re
from urllib.parse import urlparse, urlunparse

# List of approved RSS feed providers (domains or sub‑domains).
# Add or remove entries as your organization requires.
ALLOWED_DOMAINS = {
    "nytimes.com",
    "bbc.co.uk",
    "cnn.com",
    "techcrunch.com",
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "feed.ted.com",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # ::1 IPv6 loopback
        (::1)
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    # Try IPv4 first
    return bool(PRIVATE_IP_RE.match(host))

def _normalize_url(parsed: "ParseResult") -> str:
    """Return a canonical form of the URL."""
    # Force scheme to lowercase, netloc to lowercase
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path,
            "",  # params
            parsed.query,  # preserve query string if any
            "",
        )
    )

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
        A sanitized, canonicalized version of the URL if it is approved.

    Raises
    ------
    ValueError
        If the URL does not use http/https, points to a private network,
        or is not in the approved domain list.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Scheme must be http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Netloc must exist
    if not parsed.netloc:
        raise ValueError("URL missing host component")

    # Reject private IP addresses
    host = parsed.hostname
    if not host:
        raise ValueError("URL missing hostname")

    # Strip port for comparison
    host_no_port = host.lower()
    if _is_private_ip(host_no_port):
        raise ValueError("URL points to a private IP address")

    # Reject domains that are not in the whitelist
    domain_match = False
    for allowed in ALLOWED_DOMAINS:
        if host_no_port == allowed or host_no_port.endswith("." + allowed):
            domain_match = True
            break

    if not domain_match:
        raise ValueError(f"Domain '{host_no_port}' is not an approved RSS provider")

    # Return a sanitized, canonical URL
    return _normalize_url(parsed)