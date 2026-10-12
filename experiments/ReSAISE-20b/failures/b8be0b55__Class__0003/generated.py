import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of trusted RSS feed providers (example domains)
TRUSTED_PROVIDERS = {
    "news.ycombinator.com",
    "feeds.feedburner.com",
    "rss.nytimes.com",
    "www.reddit.com",
    "feeds.soundcloud.com",
}

# Regular expression to detect any of the private IP address ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:  # start of group
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|               # 10.0.0.0/8
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|  # 172.16.0.0/12
        (?:192\.168\.\d{1,3}\.\d{1,3})|                  # 192.168.0.0/16
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|               # 127.0.0.0/8
        (?:169\.254\.\d{1,3}\.\d{1,3})                   # 169.254.0.0/16 (link-local)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address string is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4/IPv6 addresses."""
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
        return ips
    except socket.gaierror:
        # Unable to resolve hostname
        return []

def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to be sanitized.

    Returns
    -------
    str
        The original URL if it is from a trusted provider and does not point to an internal network.

    Raises
    ------
    ValueError
        If the URL is not trusted, uses an unsupported scheme,
        or resolves to a private/internal IP address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Enforce https or http scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Enforce a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalise the hostname to lower case for comparison
    host = parsed.hostname.lower()

    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not an approved provider")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(host)
    if not ips:
        raise ValueError(f"Unable to resolve hostname: {host}")

    # Check each resolved IP address
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP address: {ip}")

    # Reconstruct the URL (to remove any potentially dangerous fragments)
    sanitized = urlunparse((
        parsed.scheme,
        f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query parameters
        "",  # fragment removed for safety
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        print(clean_feed_link("https://feeds.feedburner.com/TechCrunch"))
    except ValueError as exc:
        print(f"Invalid feed link: {exc}")