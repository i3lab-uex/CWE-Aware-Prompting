import re
from urllib.parse import urlparse, unquote
import ipaddress

# Approved public-facing API endpoints (hostnames or domain suffixes)
APPROVED_HOSTS = {
    "api.example.com",
    "services.company.org",
    ".trustedpartner.net",  # any subdomain of trustedpartner.net
}

# Regular expression to detect private IP ranges (RFC 1918, loopback, link-local)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (192\.168\.\d{1,3}\.\d{1,3})|
        (127\.0\.0\.1)|
        (169\.254\.\d{1,3}\.\d{1,3})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP address string is in a private or reserved range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

def _is_approved_host(host: str) -> bool:
    """
    Check whether the host matches one of the approved hosts or domain suffixes.
    """
    host = host.lower()
    for pattern in APPROVED_HOSTS:
        if pattern.startswith("."):
            # Domain suffix match
            if host.endswith(pattern):
                return True
        else:
            if host == pattern:
                return True
    return False

def manage_webhook(url_hook: str) -> str:
    """
    Validate the provided webhook URL and return it if safe.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a private/internal network address, or
                    targets an unapproved domain.
    """
    if not isinstance(url_hook, str):
        raise ValueError("Webhook URL must be a string")

    parsed = urlparse(url_hook)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize host (remove port for comparison)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Check for private IP addresses
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private IP address")

    # Resolve host to IP to guard against DNS rebinding attacks
    try:
        import socket
        ip_list = socket.getaddrinfo(hostname, None)
        for family, _, _, _, sockaddr in ip_list:
            ip_str = sockaddr[0]
            if _is_private_ip(ip_str):
                raise ValueError("Resolved IP is private or internal")
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve host: {e}")

    # Verify that the hostname is approved
    if not _is_approved_host(hostname):
        raise ValueError(f"Host '{hostname}' is not approved")

    # Reconstruct the URL to ensure it's normalized
    safe_url = parsed.geturl()
    return safe_url

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         print(manage_webhook("https://api.example.com/webhook"))
#     except ValueError as e:
#         print(f"Invalid webhook: {e}")