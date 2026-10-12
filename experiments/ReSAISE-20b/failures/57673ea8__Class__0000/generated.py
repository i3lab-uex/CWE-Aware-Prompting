import re
import socket
from urllib.parse import urlparse, urlunparse

# List of trusted RSS feed providers (hostnames or domain patterns)
TRUSTED_PROVIDERS = [
    r"^(.+\.)?rss\.nytimes\.com$",           # The New York Times
    r"^(.+\.)?feeds\.bbc\.co\.uk$",          # BBC News
    r"^(.+\.)?rss\.guardian\.com$",          # The Guardian
    r"^(.+\.)?news\.yahoo\.com$",            # Yahoo News
    r"^(.+\.)?cnn\.com$",                    # CNN
]

# Regular expression to detect private / loopback IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10|127)\."                       # 10.x.x.x or 127.x.x.x
    r"|172\.(1[6-9]|2\d|3[01])\."        # 172.16-31.x.x
    r"|192\.168\."
    r"|::1$"                             # IPv6 loopback
    r")"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is a private or loopback address."""
    # IPv4
    parts = ip.split(".")
    if len(parts) == 4:
        return PRIVATE_IP_REGEX.match(ip) is not None
    # IPv6 - check for ::1 only (loopback)
    return ip == "::1"

def _is_trusted_host(host: str) -> bool:
    """Check if the hostname matches any trusted provider pattern."""
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, host.lower()):
            return True
    return False

def validate_feed_url(url: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does
    not resolve to an internal or private IP address.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not HTTP/HTTPS, does not belong to a trusted provider,
        or resolves to an internal/private IP address.
    """
    if not url:
        raise ValueError("URL must not be empty")

    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # 1. Check provider trust
    if not _is_trusted_host(host):
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # 2. Resolve hostname to IP(s) and ensure none are private
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # 3. Rebuild URL to ensure consistency
    cleaned_url = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return cleaned_url

# Example usage (uncomment to test)
# try:
#     valid = validate_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(f"Validated URL: {valid}")
# except ValueError as e:
#     print(f"Validation failed: {e}")