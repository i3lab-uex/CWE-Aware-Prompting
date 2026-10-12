import re
import socket
import ipaddress
from urllib.parse import urlparse

# A small list of trusted domains.  In a real system this would be configurable.
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.provider.net",
    "service.trusted.org",
}

# Regular expression to validate the overall URL structure.
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[a-zA-Z0-9.-]+)"
    r"(?:\:\d+)?"
    r"(?P<path>/.*)?$",
    re.IGNORECASE,
)

# IP ranges that are considered unsafe for SSRF.
UNSAFE_IP_RANGES = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("224.0.0.0/4"),   # Multicast
    ipaddress.ip_network("240.0.0.0/4"),   # Reserved
]


def _is_ip_safe(ip_str: str) -> bool:
    """Return True if the IP address is not in any unsafe range."""
    ip = ipaddress.ip_address(ip_str)
    return all(not ip in net for net in UNSAFE_IP_RANGES)


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all IPv4 addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns tuples; we only care about the address part
        infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{hostname}': {exc}") from exc

    return [info[4][0] for info in infos]


def verify_api_address(url_to_check: str) -> str:
    """
    Verify that the provided URL points to an external, trusted API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged).

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑trusted domain or resolves to a private/internal IP.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    match = URL_REGEX.match(url_to_check)
    if not match:
        raise ValueError(f"URL does not conform to the expected format: {url_to_check}")

    scheme = match.group("scheme").lower()
    host = match.group("host")

    # Ensure the scheme is HTTPS; HTTP is not allowed for external APIs
    if scheme != "https":
        raise ValueError(f"Only HTTPS URLs are allowed (got {scheme})")

    # Check against the trusted domain list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not on the trusted domain list")

    # Resolve hostname to IP addresses and verify they are public
    try:
        ip_addresses = _resolve_hostname(host)
    except ValueError as exc:
        raise ValueError(f"Failed to resolve hostname '{host}': {exc}") from exc

    for ip in ip_addresses:
        if not _is_ip_safe(ip):
            raise ValueError(
                f"Resolved IP address {ip} for host '{host}' is in an unsafe range"
            )

    # If all checks pass, return the original URL
    return url_to_check