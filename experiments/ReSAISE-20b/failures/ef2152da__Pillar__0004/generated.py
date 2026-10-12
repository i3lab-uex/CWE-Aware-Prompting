import re
from urllib.parse import urlparse, ParseResult, urlunparse
import ipaddress

# Whitelist of approved public API endpoints (domain names or CIDR blocks)
WHITELIST = {
    "api.example.com",
    "service.myapp.io",
    "api.internal.allowed.net",
    # CIDR blocks for public ranges if needed
    ipaddress.ip_network("203.0.113.0/24"),
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)  # IPv4 private
    |(^169\.254\.)                                 # Link-local
    |(^127\.)                                      # Loopback
    |(^0\.0\.0\.0)                                  # Unspecified
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the IP string is a private or special-purpose address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_unspecified
    except ValueError:
        # Not a valid IP address, treat as non-private
        return False

def _is_whitelisted(host: str) -> bool:
    """
    Check if the host matches any entry in the whitelist.
    The whitelist may contain domain names or CIDR blocks.
    """
    # Direct domain match
    if host in WHITELIST:
        return True

    # Check against CIDR blocks
    try:
        ip = ipaddress.ip_address(host)
        for entry in WHITELIST:
            if isinstance(entry, ipaddress._BaseNetwork) and ip in entry:
                return True
    except ValueError:
        # host is not an IP address, skip CIDR check
        pass

    return False

def validate_callback(callback_url: str) -> str:
    """
    Validate a webhook callback URL ensuring it points to an approved
    public API endpoint and does not resolve to any private/internal address.

    Args:
        callback_url (str): The external webhook URL to validate.

    Returns:
        str: A sanitized and validated URL suitable for internal API calls.

    Raises:
        ValueError: If the URL domain is not in the whitelist or resolves
                    to a private/internal network address.
    """
    if not callback_url:
        raise ValueError("callback_url must be a non-empty string")

    # Parse the URL
    parsed: ParseResult = urlparse(callback_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Normalize host: strip port if present
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check for private IPs or disallowed domains
    if PRIVATE_IP_REGEX.search(host):
        raise ValueError("URL host resolves to a private or special IP address")

    # Validate against whitelist
    if not _is_whitelisted(host):
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct a safe URL preserving scheme, host, port, path, query, fragment
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized