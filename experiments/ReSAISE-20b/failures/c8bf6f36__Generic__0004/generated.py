import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A small list of approved RSS providers.
# In a real‑world scenario this would be configurable or read from a secure store.
APPROVED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regular expression to detect private IP addresses in dotted notation.
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10(?:\.\d{1,3}){3})|"
    r"(172\.1[6-9]\.\d{1,3}\.\d{1,3})|"
    r"(172\.2[0-9]\.\d{1,3}\.\d{1,3})|"
    r"(172\.3[0-1]\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(127\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_link : str
        The URL to validate.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is guaranteed to point to an approved provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider, uses a disallowed scheme,
        contains credentials, or resolves to a private/internal IP address.
    """
    if not rss_link:
        raise ValueError("RSS link must be a non-empty string")

    parsed = urlparse(rss_link)

    # Only allow http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Reject URLs that contain userinfo (username/password)
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain credentials")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Normalise the hostname to lowercase
    hostname = hostname.lower()

    if hostname not in APPROVED_PROVIDERS:
        raise ValueError(f"Unapproved provider: {hostname}")

    # Resolve the hostname to IP addresses and ensure none are private
    try:
        for addr_info in socket.getaddrinfo(hostname, None):
            ip = addr_info[4][0]
            if _is_private_ip(ip) or PRIVATE_IP_RE.match(ip):
                raise ValueError(f"Hostname {hostname} resolves to a private IP: {ip}")
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname {hostname}: {exc}") from exc

    # Reconstruct the URL without any fragment
    sanitized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, "")
    )
    return sanitized