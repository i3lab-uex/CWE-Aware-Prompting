import re
import socket
from urllib.parse import urlparse, urlunparse

# Whitelisted domains (add approved external APIs here)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.otherdomain.org",
    # Add more domains as needed
}

# Regex for detecting private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$) |          # Loopback
    (^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$) |           # Class A private
    (^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$) | # Class B private
    (^192\.168\.\d{1,3}\.\d{1,3}$)                # Class C private
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _validate_hostname(hostname: str) -> bool:
    """Check that the hostname is in the allowed domain list."""
    return any(hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_DOMAINS)

def _ensure_public_ip(hostname: str):
    """Resolve hostname to IPs and ensure none are private or loopback."""
    try:
        # Resolve all addresses (IPv4 & IPv6)
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from None

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP '{ip}', which is not allowed.")
    # If we reach here, all resolved addresses are public

def validate_service_url(service_url: str) -> str:
    """
    Validate that the given URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        Normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves to a private/internal address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: '{service_url}'")

    # Enforce https scheme to avoid potential downgrade attacks
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Only HTTPS URLs are allowed: '{service_url}'")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Could not extract hostname from URL: '{service_url}'")

    if not _validate_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of approved domains")

    _ensure_public_ip(hostname)

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(scheme="https"))
    return normalized

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://api.example.com",  # Should raise error due to http
        "https://10.0.0.5",       # Should raise error due to private IP
    ]
    for url in test_urls:
        try:
            print("Validated:", validate_service_url(url))
        except ValueError as e:
            print("Validation failed:", e)