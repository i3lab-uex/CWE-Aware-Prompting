import re
from urllib.parse import urlparse
import ipaddress

# A small whitelist of trusted RSS providers.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogspot.com",
    "wordpress.com",
    "medium.com",
    # add more trusted domains here
}

# Regular expression to match common internal IP ranges.
INTERNAL_IP_REGEX = re.compile(
    r"""
    ^
    (?:                 # non-capturing group for the various internal ranges
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |
        192\.168\.\d{1,3}\.\d{1,3} |
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the supplied IP string is a private/internal address.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        # Not a valid IP address.
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that the provided RSS feed URL comes from a trusted provider
    and does not point to an internal network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is valid and trusted.

    Raises:
        ValueError: If the URL is not from a trusted domain or resolves
                    to an internal IP address.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host is in the trusted domain list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid host")

    # Check for internal IPs directly via hostname resolution
    try:
        import socket

        # Resolve all addresses for the host
        addresses = socket.getaddrinfo(hostname, None)
        for _, _, _, _, sockaddr in addresses:
            ip = sockaddr[0]
            if _is_internal_ip(ip):
                raise ValueError("URL resolves to an internal IP address")
    except socket.gaierror:
        # Hostname could not be resolved; treat as invalid
        raise ValueError("Unable to resolve host")

    # Ensure the hostname ends with one of the trusted domains
    if not any(hostname.lower().endswith(f".{domain}") or hostname.lower() == domain
               for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{hostname}' is not from a trusted provider")

    # Finally, reject any URL that points to an internal IP directly
    if INTERNAL_IP_REGEX.match(hostname):
        raise ValueError("Hostname is an internal IP address")

    return url