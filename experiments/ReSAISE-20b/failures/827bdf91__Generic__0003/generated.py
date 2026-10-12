import re
from urllib.parse import urlparse
import socket
import ipaddress

# List of trusted RSS feed providers
_TRUSTED_PROVIDERS = {
    'rss.nytimes.com',
    'feeds.bbci.co.uk',
    'news.yahoo.com',
    'rss.cnn.com',
    'feeds.feedburner.com',
}

# Regular expression to detect IP addresses in the hostname
_IP_RE = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is private or loopback.
    """
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all associated IP addresses.
    """
    try:
        # getaddrinfo returns a list of tuples; the 4th element contains the IP
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider and
    does not point to internal or private networks.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to access a restricted network.
    """
    if not isinstance(rss_url, str):
        raise ValueError("RSS URL must be a string")

    parsed = urlparse(rss_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses directly in the URL
    if _IP_RE.match(host):
        raise ValueError("Direct IP addresses are not allowed")

    # Ensure hostname is in the trusted providers list
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Resolve the hostname to IPs and ensure none are private
    ips = _resolve_hostname(host)
    if not ips:
        raise ValueError(f"Unable to resolve hostname '{host}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to a private IP ({ip})")

    # Reconstruct the URL with only scheme and netloc (strip path/query fragments)
    sanitized = f"{parsed.scheme}://{host}"
    if parsed.port:
        sanitized += f":{parsed.port}"

    return sanitized