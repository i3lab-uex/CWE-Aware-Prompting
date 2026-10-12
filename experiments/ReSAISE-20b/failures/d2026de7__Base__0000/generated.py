import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal set of trusted RSS providers.  Extend this list as needed.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",  # example
    "rss.cnn.com",
}

# Regular expression to reject localhost or private IP addresses.
_PRIVATE_IP_RE = re.compile(
    r"""
    (^localhost$)|                               # localhost
    (^127\.)|(^10\. )|(^172\.1[6-9]\.|^172\.2[0-9]|^172\.3[0-1])|  # private IPs
    (^192\.168\.)|
    (^169\.254\.)
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_host(host: str) -> bool:
    """
    Return True if the host is a private IP address or localhost.
    """
    # First check for obvious localhost patterns
    if _PRIVATE_IP_RE.search(host):
        return True

    try:
        # If host is an IP address, check if it's private
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, treat as domain name
        return False

def check_rss_address(rss_address: str) -> str:
    """
    Validate that `rss_address` points to a trusted RSS provider.

    Parameters
    ----------
    rss_address : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or attempts to reach a
        restricted internal network.
    """
    if not rss_address:
        raise ValueError("RSS address must be a non-empty string")

    parsed = urlparse(rss_address)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject URLs with no netloc (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must include a hostname")

    host = parsed.hostname.lower()
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Reject private or local hosts
    if _is_private_host(host):
        raise ValueError("URL points to a private or local host")

    # Ensure the host is in the trusted list
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure it's properly formatted
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized