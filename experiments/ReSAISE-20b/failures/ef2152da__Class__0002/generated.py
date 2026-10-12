import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelisted public API base URLs (scheme + netloc)
WHITELIST = {
    "https://api.example.com",
    "https://service.another.org",
    "https://public.api.net",
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:  # IPv4
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (192\.168\.\d{1,3}\.\d{1,3})|
        (169\.254\.\d{1,3}\.\d{1,3})
    )
    |
    (?:  # IPv6
        (::1)|
        (fc00::/7)|
        (fd00::/8)
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _validate_host(host: str) -> bool:
    """
    Validate that the host is either a public domain in the whitelist
    or resolves to a public IP address.
    """
    # Check against whitelist first (exact match)
    for base in WHITELIST:
        if host == urlparse(base).netloc:
            return True

    # Resolve hostname to IP addresses
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            return False
    return True

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal
    API usage.

    Raises:
        ValueError: If the domain is not whitelisted or resolves to a private IP.
    """
    parsed = urlparse(callback_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Enforce HTTPS for security
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Validate host
    if not _validate_host(parsed.netloc):
        raise ValueError(f"Host '{parsed.netloc}' is not allowed")

    # Reconstruct the URL to ensure no path traversal or query tricks
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path.rstrip("/"),
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url