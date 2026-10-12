import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted RSS providers (example list – adjust as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to detect potential internal IP addresses
_INTERNAL_IP_RE = re.compile(
    r"""
    ^(?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )$
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is a public routable address.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return not (addr.is_private or addr.is_loopback or addr.is_reserved or addr.is_link_local)
    except ValueError:
        # Not a valid IP address
        return False


def _is_internal_ip(ip: str) -> bool:
    """
    Quick regex check for common internal IP patterns.
    """
    return _INTERNAL_IP_RE.match(ip) is not None


def check_rss_source(source_url: str) -> str:
    """
    Validate that the given RSS feed URL comes from a trusted provider
    and does not point to an internal network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, not trusted,
                    or resolves to an internal IP address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Normalise the hostname (lowercase, strip port)
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Check against the whitelist
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host {host}: {exc}") from exc

    # Verify that at least one resolved IP is public
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP {ip} for host {host} is internal")
        if _is_public_ip(ip):
            # Found a public IP – good to go
            break
    else:
        raise ValueError(f"All resolved IPs for {host} are non‑public")

    # Reconstruct the URL to ensure consistent formatting
    normalized_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return normalized_url