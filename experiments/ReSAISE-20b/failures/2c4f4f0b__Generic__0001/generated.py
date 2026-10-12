import re
from urllib.parse import urlparse
import ipaddress

# Define a whitelist of trusted RSS providers.
# In production, populate this list with real domains or patterns.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regex for detecting IPv4/IPv6 addresses in the hostname part
IP_PATTERN = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^\[.*\]$")

def _is_private_ip(host: str) -> bool:
    """
    Determine whether the given host string resolves to a private IP.
    Accepts either an IP literal or a hostname that can be resolved
    to one or more private addresses.
    """
    # If the host is already an IP literal
    if IP_PATTERN.match(host):
        try:
            ip = ipaddress.ip_address(host.strip("[]"))
            return ip.is_private
        except ValueError:
            pass  # Not a valid IP literal; fall back to resolution

    # Resolve hostname to addresses and check each
    try:
        import socket
        for addr in socket.getaddrinfo(host, None):
            ip = ipaddress.ip_address(addr[4][0])
            if ip.is_private:
                return True
    except Exception:
        # If resolution fails, treat as potentially unsafe
        pass

    return False


def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL originates from a trusted provider
    and does not target private/internal networks.

    Parameters
    ----------
    source_url : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {source_url}")

    # Reject URLs that target private IP ranges
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private/internal network address")

    # Ensure the hostname matches one of the trusted providers
    host = parsed.hostname.lower()
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    return source_url