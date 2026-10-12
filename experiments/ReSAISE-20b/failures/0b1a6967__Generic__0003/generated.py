import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains (add your own allowed patterns here)
ALLOWED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\..*\.mycompany\.org$",
]

# Optional: allow specific IP ranges (public) if needed
ALLOWED_IP_RANGES = [
    ipaddress.ip_network("54.0.0.0/8"),   # example AWS range
    ipaddress.ip_network("13.229.0.0/16"),  # another example range
]

# Regular expression to detect private/reserved IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        10\.|                # 10.0.0.0 – 10.255.255.255
        172\.(1[6-9]|2\d|3[0-1])\.|  # 172.16.0.0 – 172.31.255.255
        192\.168\.|          # 192.168.0.0 – 192.168.255.255
        127\.|               # localhost
        169\.254\.           # link-local
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private or reserved IP address.
    """
    try:
        # Resolve IPv4 only
        addr = ipaddress.ip_address(host)
    except ValueError:
        # Not a direct IP literal; assume it's a hostname (safe at this stage)
        return False
    if addr.is_private or addr.is_loopback or addr.is_link_local:
        return True
    # Check for reserved ranges like 0.0.0.0/8, 224.0.0.0/4 etc.
    if addr.is_reserved:
        return True
    return False

def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host matches any of the allowed domain patterns.
    """
    for pattern in ALLOWED_DOMAIN_PATTERNS:
        if re.match(pattern, host):
            return True
    return False

def _is_allowed_ip_range(host: str) -> bool:
    """
    Check if the host IP is within one of the allowed public IP ranges.
    """
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return False
    for net in ALLOWED_IP_RANGES:
        if addr in net:
            return True
    return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that a given URL is safe to call from the server.

    Parameters
    ----------
    endpoint_address : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private or internal address, or
        does not match any approved domain/IP range.
    """
    # Basic URL parsing
    parsed = urlparse(endpoint_address)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Separate hostname and port
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid hostname")

    # Reject obvious private IP literals
    if PRIVATE_IP_RE.match(host):
        raise ValueError("URL points to a private IP address")

    # If host is an IP literal, perform further checks
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private IP address")
        if not _is_allowed_ip_range(host):
            raise ValueError("IP address is not in an allowed range")

    # If host is a domain name, check whitelist
    else:
        if not _is_allowed_domain(host):
            raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Reconstruct URL to ensure no fragments or params that could alter behavior
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,  # keep query as is
            "",  # fragment removed
        )
    )

    return cleaned