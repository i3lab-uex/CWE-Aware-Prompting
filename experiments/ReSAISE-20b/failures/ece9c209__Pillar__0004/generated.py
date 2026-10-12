import re
import socket
from urllib.parse import urlparse, urlunparse

# Define a list of allowed API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "secure.api.company.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1|
        fc00::/7|          # Unique local addresses
        fe80::/10          # Link‑local addresses
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is a private or loopback address.
    Supports both IPv4 and IPv6.
    """
    # Try to resolve the IP into a string representation
    try:
        if ":" in ip:  # IPv6
            return PRIVATE_IP_REGEX.match(ip) is not None
        else:          # IPv4
            octets = ip.split(".")
            if len(octets) != 4:
                return False
            a, b, c, d = map(int, octets)
            if 10 <= a <= 10:
                return True
            if a == 172 and 16 <= b <= 31:
                return True
            if a == 192 and b == 168:
                return True
            if ip == "127.0.0.1":
                return True
    except Exception:
        pass
    return False

def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host is in the allowed domain list or a sub‑domain of one.
    """
    host = host.lower()
    return any(
        host == domain or host.endswith("." + domain)
        for domain in ALLOWED_DOMAINS
    )

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is deemed safe and trusted.

    Raises
    ------
    ValueError
        If the URL does not belong to an allowed domain or attempts to resolve
        to a private/internal network address.
    """
    if not api_url:
        raise ValueError("API URL must not be empty")

    parsed = urlparse(api_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Resolve host to IP(s) and check for private addresses
    try:
        ips = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname: {exc}") from None

    for info in ips:
        ip_address = info[4][0]
        if _is_private_ip(ip_address):
            raise ValueError(f"Hostname resolves to private IP: {ip_address}")

    # Verify domain whitelist
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the allowed list")

    # Re‑construct URL to avoid potential manipulation (e.g., missing port)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned