import re
from urllib.parse import urlparse, urlunparse
import socket

# List of trusted domains (subdomains are allowed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regular expression for detecting private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.|                       # 10.0.0.0 – 10.255.255.255
        192\.168\.|                 # 192.168.0.0 – 192.168.255.255
        172\.(?:1[6-9]|2[0-9]|3[01])\.  # 172.16.0.0 – 172.31.255.255
        127\.|                      # localhost
        169\.254\.|                 # link-local
        0\.|                        # unspecified
        100\.64\.|                  # Carrier-grade NAT (RFC6598)
        192\.0\.2\.|                # TEST-NET-1
        198\.51\.100\.|             # TEST-NET-2
        203\.0\.113\.               # TEST-NET-3
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def _hostname_is_trusted(hostname: str) -> bool:
    """Check if the hostname ends with one of the trusted domains."""
    return any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS)


def _is_internal_hostname(hostname: str) -> bool:
    """Detect if the hostname resolves to a private IP."""
    try:
        # Resolve all addresses (IPv4 and IPv6)
        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0]
            if _is_private_ip(ip):
                return True
    except socket.gaierror:
        # If the hostname cannot be resolved, treat it as unsafe
        return True
    return False


def clean_feed_link(rss_link: str) -> str:
    """
    Sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be sanitized.

    Returns
    -------
    str
        The sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not resolve to a trusted domain,
        or resolves to an internal network address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    # Parse the URL
    parsed = urlparse(rss_link.strip())

    # Enforce HTTPS scheme
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    hostname = parsed.hostname.lower()

    # Check against trusted domains
    if not _hostname_is_trusted(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers")

    # Detect internal network access
    if _is_internal_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' resolves to an internal or private IP address")

    # Rebuild the URL to ensure no userinfo or port is present
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.hostname,  # no port or userinfo
            parsed.path or "",
            "",  # params
            parsed.query,
            "",  # fragment
        )
    )

    return sanitized