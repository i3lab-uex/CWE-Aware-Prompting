import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a whitelist of trusted RSS providers (scheme + netloc)
TRUSTED_PROVIDERS = {
    ('https', 'news.google.com'),
    ('https', 'rss.nytimes.com'),
    ('https', 'feeds.bbci.co.uk'),
    ('https', 'rss.cnn.com'),
    # add more providers as needed
}

# Regular expression to detect private IP address ranges (RFC1918, etc.)
PRIVATE_IP_RE = re.compile(
    r'''
    (^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|^169\.254\.)
    ''',
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (likely a hostname)
        return False

def _is_internal_hostname(hostname: str) -> bool:
    """Detect if a hostname resolves to an internal IP range."""
    # Quick regex check for obvious private IP patterns
    if PRIVATE_IP_RE.search(hostname):
        return True

    # Attempt to resolve the hostname to IPs and check each
    try:
        import socket
        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0]
            if _is_private_ip(ip):
                return True
    except Exception:
        # If resolution fails, assume it's not internal
        pass

    return False

def check_rss_source(source_url: str) -> str:
    """
    Validate that a given RSS feed URL originates from a trusted provider
    and does not point to an internal network.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is valid and trusted.

    Raises:
        ValueError: If the URL is not from a trusted provider or points to an internal address.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)

    # Basic scheme check
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize host (case-insensitive)
    hostname = parsed.hostname.lower() if parsed.hostname else ''

    # Check against whitelist
    if (parsed.scheme, hostname) not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Ensure hostname is not internal
    if _is_internal_hostname(hostname):
        raise ValueError(f"Hostname resolves to an internal address: {hostname}")

    # Reconstruct the URL to ensure no malicious fragments
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        '',  # params
        parsed.query or '',
        ''   # fragment removed
    ))

    return safe_url