import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a set of approved domain patterns (regex or exact strings)
ALLOWED_DOMAINS = {
    re.compile(r"^api\.example\.com$"),
    re.compile(r"^service\.trusted‑partner\.org$"),
}

# List of IP network ranges that are considered internal
INTERNAL_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # loopback
    ipaddress.ip_network("::1/128"),      # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),     # Unique local address (ULA)
]


def _is_ip_address(host: str) -> bool:
    """
    Determine if the host string is an IP address.
    """
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_internal_ip(ip_str: str) -> bool:
    """
    Check if the given IP string belongs to any internal network.
    """
    ip_obj = ipaddress.ip_address(ip_str)
    return any(ip_obj in net for net in INTERNAL_NETWORKS)


def _is_allowed_domain(host: str) -> bool:
    """
    Verify that the host matches one of the approved domain patterns.
    """
    for pattern in ALLOWED_DOMAINS:
        if pattern.match(host):
            return True
    return False


def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the supplied API endpoint is safe to call.

    The function performs the following checks:
        1. URL must have a scheme of http or https.
        2. Hostname must resolve to an external IP address that is not in
           internal/private ranges.
        3. Hostname must match one of the approved domain patterns.

    If all checks pass, the original URL is returned unchanged.
    Otherwise a ValueError is raised.

    Args:
        api_endpoint: The URL string to validate.

    Returns:
        str: The validated and unchanged URL.

    Raises:
        ValueError: If the URL is malformed, points to a private network,
                    or does not match an approved domain.
    """
    # Parse the URL
    parsed = urlparse(api_endpoint)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve IP address (if the host is an IP literal)
    if _is_ip_address(host):
        if _is_internal_ip(host):
            raise ValueError(f"IP address {host} is internal or private")
    else:
        # For domain names, ensure they are in the approved list
        if not _is_allowed_domain(host):
            raise ValueError(f"Domain {host} is not approved")

    # Reconstruct the URL to avoid any subtle injection
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))

    return safe_url