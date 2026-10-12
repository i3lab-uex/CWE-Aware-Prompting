import re
from urllib.parse import urlparse
import socket
import ipaddress

# List of trusted providers' domains (add more as needed)
TRUSTED_DOMAINS = [
    r"^feeds\.bbc\.co\.uk$",
    r"^rss\.cnn\.com$",
    r"^news\.yahoo\.com$",
    r"^rss\.guardian\.com$",
    r"^api\.reddit\.com$",
]

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.0\.0\.1$|                # Loopback
     ^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$| # Class A private
     ^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$| # Class B private
     ^192\.168\.\d{1,3}\.\d{1,3}$)   # Class C private
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP is in a private/reserved range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # If the string is not a valid IP address, treat as non‑private
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4 addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
        return [sockaddr[0] for _, _, _, _, sockaddr in infos]
    except socket.gaierror:
        # If resolution fails, treat as invalid
        return []

def check_rss_source(source_url: str) -> str:
    """
    Validate that an RSS feed URL originates from a trusted provider
    and does not point to an internal network address.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not from a trusted domain or resolves to an internal IP.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)

    # Basic URL sanity checks
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Check against trusted domain patterns
    host = parsed.hostname.lower()
    if not any(re.match(pattern, host) for pattern in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Resolve hostname to IPs and ensure none are private
    ips = _resolve_hostname(host)
    if not ips:
        raise ValueError(f"Unable to resolve hostname '{host}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # All checks passed
    return source_url