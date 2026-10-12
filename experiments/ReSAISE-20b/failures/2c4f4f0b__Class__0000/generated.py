import re
import socket
from urllib.parse import urlparse

# List of trusted RSS providers (example domains). Extend as needed.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "feeds.reuters.com",
    "rss.cnn.com",
}

# Regular expression to detect private or loopback IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^(
        10\.|                         # 10.0.0.0/8
        127\.|                        # 127.0.0.0/8 (loopback)
        169\.254\.|                   # 169.254.0.0/16 (link-local)
        172\.(1[6-9]|2[0-9]|3[01])\.| # 172.16.0.0/12
        192\.168\.                    # 192.168.0.0/16
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    return bool(PRIVATE_IP_RE.match(ip))


def _hostname_is_trusted(hostname: str) -> bool:
    """Check if the hostname is in the trusted domain list."""
    # Normalize subdomains: check suffix matching
    for domain in TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc


def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL originates from a trusted provider and does not
    target internal network addresses.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the hostname is not trusted,
        or if any resolved IP address belongs to a private/loopback range.
    """
    # Basic URL parsing
    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Check that the hostname is from a trusted domain
    if not _hostname_is_trusted(hostname.lower()):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_hostname(hostname)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for hostname '{hostname}' is private or loopback")

    # All checks passed; return the original URL
    return source_url