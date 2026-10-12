import re
from urllib.parse import urlparse
import ipaddress

# List of trusted RSS providers (hostnames or regex patterns)
TRUSTED_PROVIDERS = [
    re.compile(r"^rss\.nytimes\.com$"),
    re.compile(r"^feeds\.bbci\.co\.uk$"),
    re.compile(r"^news\.cnet\.com$"),
    # Add more providers as needed
]

# Regex to reject URLs that contain localhost or private IPs
LOCALHOST_RE = re.compile(r"(^localhost$|^127\.0\.0\.1$)", re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider
    and does not point to an internal network address.

    Parameters
    ----------
    url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL is not trusted or points to a private/internal address.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # Reject localhost or private IPs
    if LOCALHOST_RE.match(host):
        raise ValueError("URL points to localhost")

    # Resolve IP if hostname is numeric
    try:
        ip_addr = str(ipaddress.ip_address(host))
        if _is_private_ip(ip_addr):
            raise ValueError("URL resolves to a private IP address")
    except ValueError:
        # Hostname is not an IP; attempt to resolve it
        import socket
        try:
            for ip in socket.getaddrinfo(host, None):
                ip_str = ip[4][0]
                if _is_private_ip(ip_str):
                    raise ValueError("URL resolves to a private IP address")
        except socket.gaierror:
            # Hostname could not be resolved; treat as unsafe
            raise ValueError("Hostname could not be resolved")

    # Verify host against trusted providers list
    if not any(pattern.match(host) for pattern in TRUSTED_PROVIDERS):
        raise ValueError(f"Untrusted provider: {host}")

    # All checks passed
    return url