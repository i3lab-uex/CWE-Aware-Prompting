import socket
import ipaddress
from urllib.parse import urlparse

# List of trusted RSS feed providers (add or remove as needed)
TRUSTED_HOSTNAMES = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is private or reserved.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; treat as non-private for safety.
        return False

def _is_internal_hostname(hostname: str) -> bool:
    """
    Resolve the hostname and check if any resolved IP is private.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If we cannot resolve the hostname, treat it as unsafe.
        return True

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            return True
    return False

def validate_feed_url(url: str) -> str:
    """
    Validate that the given RSS feed URL comes from a trusted provider and
    does not point to an internal network address.

    Parameters:
        url (str): The RSS feed URL to validate.

    Returns:
        str: The validated URL if it is trusted and external.

    Raises:
        ValueError: If the URL does not belong to a trusted provider or
                    resolves to an internal network address.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url}")

    hostname = parsed.hostname.lower()
    if hostname not in TRUSTED_HOSTNAMES:
        raise ValueError(f"Untrusted provider: {hostname}")

    if _is_internal_hostname(hostname):
        raise ValueError(f"Hostname resolves to an internal IP: {hostname}")

    # Reconstruct the URL to ensure consistent formatting
    return parsed.geturl()