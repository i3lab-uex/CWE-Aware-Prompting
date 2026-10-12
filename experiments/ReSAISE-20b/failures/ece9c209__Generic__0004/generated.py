import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of trusted API domains (add your own as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "trusted.api.net"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.)|                # localhost
    (^10\.)|                 # private network
    (^172\.1[6-9]\.)|        # 172.16–172.31
    (^172\.2[0-9]\.)|
    (^172\.3[0-1]\.)|
    (^192\.168\.)            # private network
    """,
    re.VERBOSE
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address; let caller handle it
        return False

def _is_allowed_domain(host: str) -> bool:
    """Check if the host is in the allowed domains list."""
    return any(host == domain or host.endswith(f".{domain}") for domain in ALLOWED_DOMAINS)

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that a URL points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private IP,
        or its domain is not in the allowed list.
    """
    if not api_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(api_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Resolve potential percent-encoding
    host = unquote(parsed.hostname)

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Reject internal domain patterns (like .local, .internal)
    if re.search(r'\.(local|internal)\.?$', host):
        raise ValueError(f"URL points to an internal domain: {host}")

    # Domain must be in the allowed list
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of allowed API domains")

    # If all checks pass, return the normalized URL
    return parsed.geturl()