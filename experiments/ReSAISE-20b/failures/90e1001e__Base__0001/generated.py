import re
from urllib.parse import urlparse, unquote
import socket
import ipaddress

# List of approved domains (can be expanded)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.goodprovider.io",
    "data.safeapi.org",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|                # loopback
     ^10\.|                 # Class A private
     ^192\.168\.|           # Class C private
     ^172\.(1[6-9]|2\d|3[0-1])\.   # Class B private
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., hostname)
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4 addresses."""
    try:
        _, _, ipaddrs = socket.gethostbyname_ex(hostname)
        return ipaddrs
    except socket.gaierror:
        # Host could not be resolved
        return []


def validate_service_url(service_url: str) -> str:
    """
    Validate that the provided URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a non‑approved domain,
        or resolves to an internal/private IP address.
    """
    # Basic URL parsing
    parsed = urlparse(service_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {service_url}")

    # Normalise hostname (lowercase, strip port)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError(f"URL does not contain a valid host: {service_url}")

    # Check domain against approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IP addresses
    ip_addresses = _resolve_hostname(hostname)
    if not ip_addresses:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    # Ensure none of the IPs are private or reserved
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to private IP {ip}"
            )

    # Additional safety: reject URLs that resolve to localhost via '127.0.0.1' or '::1'
    if any(ip in ("127.0.0.1", "::1") for ip in ip_addresses):
        raise ValueError(f"Hostname '{hostname}' resolves to localhost")

    # URL passed all checks
    return service_url

# Example usage (uncomment to test):
# try:
#     valid_url = validate_service_url("https://api.example.com/v1/resource")
#     print(f"Validated URL: {valid_url}")
# except ValueError as e:
#     print(f"Validation error: {e}")