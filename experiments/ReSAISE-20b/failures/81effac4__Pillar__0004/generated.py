import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A set of domains that are explicitly trusted for external API access.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.vendor.com",
    "public-api.cloudprovider.net",
}

# Regular expression to detect IP addresses in URLs.
IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def _is_private_ip(ip: str) -> bool:
    """
    Determine whether the given IP address is in a private, loopback,
    or reserved range as defined by RFC 1918 and related standards.
    """
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local or \
               ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # If the string is not a valid IP, treat it as non-private.
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all of its IPv4 addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [info[4][0] for info in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)]

def check_api_link(api_link: str) -> str:
    """
    Validate that the provided API link points to a trusted external domain
    and does not resolve to an internal or private IP address.

    Args:
        api_link: The API URL to be verified.

    Returns:
        The validated URL, unchanged if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, points to an untrusted domain,
                    or resolves to a private/internal IP address.
    """
    # Basic URL parsing and validation
    parsed = urlparse(api_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {api_link}")

    # Enforce HTTPS for external API calls
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Only HTTPS URLs are allowed: {api_link}")

    # Extract hostname and port
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError(f"URL missing hostname: {api_link}")

    # Check against the trusted domain whitelist
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the trusted list")

    # Resolve hostname to IP addresses and ensure none are private
    try:
        ip_list = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for '{hostname}': {exc}") from exc

    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # Reconstruct the URL to ensure canonical form
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return cleaned

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         print(check_api_link("https://api.example.com/v1/resource"))
#     except ValueError as e:
#         print(f"Validation error: {e}")