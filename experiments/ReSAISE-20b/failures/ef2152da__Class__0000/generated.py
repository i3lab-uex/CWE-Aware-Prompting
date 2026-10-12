import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API base URLs (scheme + netloc)
WHITELIST = {
    "https://api.example.com",
    "https://public-api.service.org",
}

# Regex for private IP ranges (IPv4 & IPv6)
PRIVATE_IP_REGEX = re.compile(
    r"""
    (
        # IPv4 private ranges
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (192\.168\.\d{1,3}\.\d{1,3})|
        # IPv6 unique local addresses
        ([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
    )
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Check if the given IP string is a private address.
    Handles both IPv4 and IPv6.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If not a valid IP address, treat as non‑private (will be caught elsewhere)
        return False

def validate_callback(callback_url: str) -> str:
    """
    Validate that a callback URL is from an approved public API endpoint
    and does not resolve to a private/internal network address.

    Parameters:
        callback_url (str): The external webhook URL to validate.

    Returns:
        str: The original validated URL, suitable for internal API calls.

    Raises:
        ValueError: If the URL is not whitelisted or resolves to a private IP.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)

    # Basic URL validation
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {callback_url}")

    # Ensure scheme is HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Reconstruct the base URL to compare with whitelist
    base_url = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"
    if base_url not in WHITELIST:
        raise ValueError(f"Domain {parsed.netloc} is not whitelisted")

    # Resolve hostname to IP addresses
    try:
        host_ips = socket.gethostbyname_ex(parsed.hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname {parsed.hostname}") from exc

    # Reject if any IP is private
    for ip in host_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {parsed.hostname} resolves to private IP {ip}")

    # Ensure the path is present (some APIs might require a specific endpoint)
    if not parsed.path:
        raise ValueError("URL must include a path component")

    # Return the canonical URL (re‑encoded)
    return urlunparse(parsed)

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_callback("https://api.example.com/v1/notify")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Validation failed: {e}")