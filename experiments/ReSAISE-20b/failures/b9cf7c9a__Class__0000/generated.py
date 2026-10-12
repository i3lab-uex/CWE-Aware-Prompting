import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A simple whitelist of approved domains.  In a real system this would
# likely be loaded from configuration or an external service.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.acme.org",
    "data.partner.net",
}

# Regular expression to match private and local network ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^|,)\s*
    (?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1|
        [fF][cC][0-9a-fA-F]{2}:
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is private or local.
    Handles both IPv4 and IPv6.
    """
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _resolve_host(hostname: str) -> list[str]:
    """
    Resolve the hostname to all its IPv4 and IPv6 addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    return [info[4][0] for info in infos]

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL supplied by the caller.

    Returns
    -------
    str
        The normalized URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to a non‑approved domain,
        resolves to a private/internal IP address,
        or fails any other safety check.
    """
    # Parse the URL
    parsed = urlparse(endpoint_url)

    # Basic scheme check – only https is allowed to prevent
    # accidental use of file:// or other dangerous schemes.
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Only HTTPS URLs are allowed; got scheme '{parsed.scheme}'")

    # Ensure there is a hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against the approved domain list (case‑insensitive)
    if parsed.hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not on the approved list")

    # Resolve hostname to IP addresses
    ips = _resolve_host(parsed.hostname)

    # Ensure none of the resolved IPs are private or loopback
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP address '{ip}' for hostname '{parsed.hostname}' is private or local")

    # Re‑assemble the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(scheme="https"))
    return normalized

# Example usage (commented out – remove for production code)
# try:
#     api_url = check_api_url("https://api.example.com/v1/data")
#     print(f"Validated URL: {api_url}")
# except ValueError as exc:
#     print(f"URL validation failed: {exc}")