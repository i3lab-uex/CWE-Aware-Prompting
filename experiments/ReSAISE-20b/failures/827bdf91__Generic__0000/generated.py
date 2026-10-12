import re
from urllib.parse import urlparse, ParseResult
import socket
import ipaddress

# List of fully‑qualified domains that are allowed to provide RSS feeds.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
    # add more trusted domains here
}

# Regular expression to detect private IP ranges (RFC1918 + loopback)
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.|^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)   # IPv4 private
    |(^::1$)                                                # IPv6 loopback
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or localhost.
    The function tries to resolve the hostname; if resolution fails
    we conservatively treat it as unsafe.
    """
    try:
        addr_info = socket.getaddrinfo(host, None, family=socket.AF_UNSPEC)
    except socket.gaierror:
        # Cannot resolve hostname – treat as unsafe
        return True

    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if PRIVATE_IP_RE.match(ip):
            return True
    return False


def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL, ensuring it originates from a trusted provider
    and does not point to internal or private networks.

    Parameters
    ----------
    rss_url : str
        The URL of the RSS feed to be validated.

    Returns
    -------
    str
        A sanitized, fully‑qualified RSS feed URL that has passed validation.

    Raises
    ------
    ValueError
        If the URL is not HTTP/HTTPS, does not resolve to a trusted provider,
        or resolves to an internal/private IP address.
    """
    if not isinstance(rss_url, str):
        raise ValueError("rss_url must be a string")

    parsed: ParseResult = urlparse(rss_url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Netloc (hostname) must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject localhost or loopback addresses directly
    if parsed.hostname.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError("Access to localhost is prohibited")

    # Check if hostname resolves to a private IP
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or internal network address")

    # Enforce trusted provider domain
    if parsed.hostname.lower() not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not a trusted provider")

    # Reconstruct the URL to ensure no query parameters or fragments
    sanitized_url = f"{parsed.scheme}://{parsed.hostname}"
    if parsed.port:
        sanitized_url += f":{parsed.port}"
    sanitized_url += parsed.path

    return sanitized_url