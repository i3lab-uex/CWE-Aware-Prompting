import re
from urllib.parse import urlparse
import socket
import ipaddress

# Trusted RSS providers (domain names or hostname patterns)
TRUSTED_PROVIDERS = [
    r"^news\.yahoo\.com$",
    r"^feeds\.bbc\.co\.uk$",
    r"^rss\.cnn\.com$",
    r"^feeds\.reuters\.com$",
    # Add more trusted providers here
]

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                                 # non-capturing group for the whole address
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname), assume not private
        return False

def _hostname_allowed(hostname: str) -> bool:
    """Check if the hostname matches any trusted provider pattern."""
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, hostname.lower()):
            return True
    return False

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider
    and does not point to an internal network.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is valid and trusted.

    Raises:
        ValueError: If the URL does not belong to a trusted provider,
                    or if it resolves to an internal/private IP.
    """
    # Basic URL parsing
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Unable to extract hostname from URL")

    # 1. Ensure the hostname is in the trusted list
    if not _hostname_allowed(hostname):
        raise ValueError(f"Hostname '{hostname}' is not a trusted provider")

    # 2. Resolve hostname to IP(s) and check for private addresses
    try:
        host_ips = socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for ip in host_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    return url