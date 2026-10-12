import re
from urllib.parse import urlparse, unquote
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted providers – add or remove domains as needed
_TRUSTED_DOMAINS = {
    "feeds.nytimes.com",
    "rss.cnn.com",
    "news.google.com/rss",
    "feeds.reuters.com",
    # Add more trusted domains here
}

# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _is_internal_hostname(hostname: str) -> bool:
    """
    Detect internal hostnames that should be blocked.
    This includes localhost, 127.0.0.1, ::1 and any hostname that resolves
    to a private IP address.
    """
    # Directly check common internal names
    if hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
        return True

    # Try to resolve the hostname to an IP address
    try:
        import socket
        for addrinfo in socket.getaddrinfo(hostname, None):
            ip = addrinfo[4][0]
            if _is_private_ip(ip):
                return True
    except Exception:
        # If resolution fails we err on the side of caution and block it.
        return True

    return False


def _is_trusted_domain(hostname: str) -> bool:
    """Check if the hostname ends with one of the trusted domains."""
    # Normalize hostname (remove port if present)
    host = hostname.split(":")[0].lower()
    for domain in _TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def check_rss_source(source_url: str) -> str:
    """
    Validate an RSS feed URL ensuring it originates from a trusted provider
    and does not target internal network addresses.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated and normalized RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal address, or
        does not belong to a trusted provider.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    # Parse the URL
    parsed = urlparse(source_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Block internal hostnames or private IPs
    if _is_internal_hostname(parsed.hostname):
        raise ValueError(f"URL points to an internal address: {parsed.hostname}")

    # Ensure the hostname is from a trusted domain
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not from a trusted provider")

    # Reconstruct the URL to avoid subtle injection via path or query
    normalized_url = parsed._replace(path=unquote(parsed.path), params="", query="", fragment="").geturl()

    return normalized_url