import re
from urllib.parse import urlparse, urlunparse

# A simple whitelist of trusted domains. In a real system this would be
# configurable, probably read from a secure config file or environment.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.net",
    "data.provider.org",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # Loopback
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 loopback
        (?:::1) |
        # IPv6 unique local addresses
        (?:fc00:|fd00:)
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Check whether the supplied host is a private IP address.
    Handles both IPv4 and IPv6.
    """
    # Strip port if present
    host = host.split(":")[0]
    # Try to interpret as IP; if it fails, assume it's a hostname
    try:
        import ipaddress

        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address – rely on regex for IPv6 special cases
        return bool(PRIVATE_IP_REGEX.match(host))


def check_api_link(api_link: str) -> str:
    """
    Validate that the provided API link points to a trusted external domain
    and does not target internal or private network addresses.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The validated, normalized URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or attempts to reach a private/internal network.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    # Parse the URL
    parsed = urlparse(api_link)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Ensure a hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject private or loopback IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or loopback address")

    # Reject if the hostname is not in the whitelist
    host_lower = parsed.hostname.lower()
    if host_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host_lower}' is not trusted")

    # Reconstruct the URL to ensure it has no path traversal or fragments
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url