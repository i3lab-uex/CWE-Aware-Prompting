import re
import socket
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of domains that are considered trusted.
ALLOWED_DOMAINS = [
    r"^api\.trustedservice\.com$",
    r"^external\.partner\.org$",
    # Add more patterns as needed
]

# Regular expression to detect potentially dangerous hostnames.
# This will reject any hostname that looks like an IP address
# or a domain containing IP-like patterns (e.g., 10.0.0.1, localhost).
IP_ADDRESS_REGEX = re.compile(r"""
    ^
    (?:[0-9]{1,3}\.){3}[0-9]{1,3}        # IPv4
    |
    \[?[a-f0-9:]+\]?                    # IPv6 (optional brackets)
    $
""", re.VERBOSE | re.IGNORECASE)


def _is_allowed_domain(hostname: str) -> bool:
    """Check if the hostname matches one of the allowed domain patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, hostname, re.IGNORECASE):
            return True
    return False


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or otherwise reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved or addr.is_multicast
    except ValueError:
        # Not a valid IP address string
        return False


def _resolve_host_to_ip(hostname: str) -> str:
    """Resolve the hostname to an IP address, raising if resolution fails."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the provided URL points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (unchanged if valid).

    Raises
    ------
    ValueError
        If the URL is not part of an allowed domain, resolves to a private or reserved IP,
        or otherwise fails validation.
    """
    # Parse the URL and ensure it uses http/https
    parsed: ParseResult = urlparse(api_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname.")

    # 1. Reject obvious IP addresses or localhost-like names
    if IP_ADDRESS_REGEX.match(hostname):
        raise ValueError("Hostname must not be an explicit IP address or localhost-like string.")

    # 2. Resolve hostname to IP and check for private/reserved addresses
    ip = _resolve_host_to_ip(hostname)
    if _is_private_ip(ip):
        raise ValueError(f"Hostname '{hostname}' resolves to private IP address {ip}.")

    # 3. Verify that the hostname is in the list of allowed domains
    if not _is_allowed_domain(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of allowed domains.")

    # If all checks pass, return the original URL
    return api_url