import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted domains or domain patterns (simple exact match for demo)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "api.anotherservice.org",
    "v1.thirdparty.io",
}

# IPv4/IPv6 private and reserved ranges
PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private/reserved range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return True  # treat invalid IP as private to be safe
    for rng in PRIVATE_RANGES:
        if ip_obj in rng:
            return True
    return False


def _resolve_host_to_ip(host: str) -> list[str]:
    """Return a list of resolved IP addresses for the host."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host '{host}': {exc}") from None


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API and is not
    resolving to any internal/private network addresses.

    Parameters:
        url_to_check (str): The URL to validate.

    Returns:
        str: The validated, normalized URL.

    Raises:
        ValueError: If the URL is malformed, points to a non-whitelisted domain,
                    or resolves to an internal/private IP address.
    """
    # Parse the URL
    parsed = urlparse(url_to_check)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url_to_check}")

    # Normalize scheme to https for external APIs
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{scheme}'")

    host = parsed.hostname.lower()

    # Check against whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Resolve host to IP(s) and ensure none are private
    ips = _resolve_host_to_ip(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is private/internal")

    # Reconstruct a clean URL (strip credentials if any)
    cleaned = parsed._replace(
        username=None,
        password=None,
        fragment="",
    )
    return urlunparse(cleaned)


# Example usage (commented out for safety)
# try:
#     safe_url = verify_api_link("https://api.example.com/v1/data")
#     print(f"Safe URL: {safe_url}")
# except ValueError as e:
#     print(f"URL validation failed: {e}")