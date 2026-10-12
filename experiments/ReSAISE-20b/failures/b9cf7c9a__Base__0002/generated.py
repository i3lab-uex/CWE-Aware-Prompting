import re
import socket
from urllib.parse import urlparse

# List of approved domains (wildcards allowed with simple regex)
APPROVED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",
    r"^service\.trusted\.org$",
    r"^api\.partner\d+\.net$",  # e.g., api.partner1.net, api.partner2.net
]

# IP address ranges that are considered private or local (RFC1918, loopback, link-local)
PRIVATE_IP_RANGES = [
    re.compile(r"^10\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^127\."),
    re.compile(r"^169\.254\."),
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or local range."""
    for pattern in PRIVATE_IP_RANGES:
        if pattern.match(ip):
            return True
    return False


def _is_approved_domain(hostname: str) -> bool:
    """Return True if the hostname matches one of the approved domain patterns."""
    for pattern in APPROVED_DOMAIN_PATTERNS:
        if re.match(pattern, hostname):
            return True
    return False


def check_api_url(endpoint_url: str) -> str:
    """
    Validate that the given URL points to an approved external API and is not
    targeting internal network addresses.

    Parameters:
        endpoint_url (str): The URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a non-approved domain, or resolves to a private IP.
    """
    # Basic URL parsing
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Check that the domain is approved
    if not _is_approved_domain(parsed.hostname.lower()):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the approved list")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname: {exc}") from exc

    # Ensure at least one resolved IP is not private
    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if not _is_private_ip(ip):
            # Found a public IP; validation passes
            return endpoint_url

    raise ValueError("Resolved IP addresses are all private or internal")


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         valid_url = check_api_url("https://api.example.com/data")
#         print(f"URL is valid: {valid_url}")
#     except ValueError as e:
#         print(f"URL validation failed: {e}")