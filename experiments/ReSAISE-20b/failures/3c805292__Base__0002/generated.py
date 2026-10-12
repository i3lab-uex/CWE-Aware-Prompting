import re
from urllib.parse import urlparse, urlunparse, ParseResult
import socket
import ipaddress

# List of allowed hostnames (case‑insensitive)
TRUSTED_HOSTS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.reddit.com",
    "feeds.theguardian.com",
}

# Regex to detect IP addresses in the host part
IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If the string is not a valid IP, treat it as non‑private
        return False

def _is_allowed_host(host: str) -> bool:
    """Check if host is in the whitelist or resolves to a public IP."""
    # Normalise case
    host_lc = host.lower()
    if host_lc in TRUSTED_HOSTS:
        return True

    # Resolve hostname to IPs
    try:
        addresses = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False

    for _, _, _, _, sockaddr in addresses:
        ip = sockaddr[0]
        if not _is_private_ip(ip):
            return True
    return False

def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to access a private network.
    """
    if not feed_address:
        raise ValueError("Feed address must be a non‑empty string")

    parsed = urlparse(feed_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with IP addresses that are private or reserved
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Detect numeric IP addresses
    if IP_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError("Access to private IP addresses is forbidden")
        # Public IPs are allowed only if in the whitelist
        if host not in TRUSTED_HOSTS:
            raise ValueError("IP address is not in the trusted list")

    # Validate hostname against whitelist or public resolution
    if not _is_allowed_host(host):
        raise ValueError(f"Hostname '{host}' is not trusted")

    # Re‑construct the URL to ensure no fragments or query parameters
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=host if not parsed.port else f"{host}:{parsed.port}",
        path=parsed.path or "/",
        params="",
        query="",
        fragment=""
    )
    return urlunparse(sanitized)