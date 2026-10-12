import re
import socket
from urllib.parse import urlparse, ParseResult

# List of trusted domains/subdomains.  Adjust as required.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.partner.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0/8
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0/12
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0/16
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0/8 (loopback)
        (?:127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 loopback ::1
        (?:::1)
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or loopback range."""
    return bool(PRIVATE_IP_RE.match(ip))


def _is_trusted_domain(hostname: str) -> bool:
    """Check if the hostname is within the trusted domain list."""
    # Normalize: strip trailing dot, convert to lower case
    hostname = hostname.rstrip(".").lower()
    # Direct match or subdomain of a trusted domain
    for t in TRUSTED_DOMAINS:
        if hostname == t or hostname.endswith("." + t):
            return True
    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private/internal address,
        or does not belong to an approved domain.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(url_to_check)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Separate hostname and port
    host, _, _ = parsed.netloc.partition(":")
    if not host:
        raise ValueError("Hostname could not be determined.")

    # Resolve the hostname to IP(s) and ensure none are private
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in addrinfo:
        # sockaddr can be (address, port) for IPv4 or IPv6
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"URL resolves to a private or internal IP address: {ip}")

    # Ensure the hostname is within trusted domains
    if not _is_trusted_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains.")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    cleaned = parsed._replace(
        netloc=host if not parsed.port else f"{host}:{parsed.port}"
    )
    return cleaned.geturl()