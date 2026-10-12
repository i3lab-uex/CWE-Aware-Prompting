import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A whitelist of domains that are considered safe for external API calls.
ALLOWED_DOMAINS = {
    "api.example.com",
    "data.provider.net",
    "services.thirdparty.org",
}

# Regex to detect private IP ranges (RFC1918, link-local, loopback, etc.).
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^|[^\d])                     # start or non-digit
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}|
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}
    )
    (?:[^\d]|$)                     # end or non-digit
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback or link‑local range.
    """
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
            ip
        ).is_loopback or ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _hostname_is_allowed(hostname: str) -> bool:
    """
    Check if the hostname is in the allowed domain list or resolves to a public IP.
    """
    # Direct match with whitelist
    if hostname in ALLOWED_DOMAINS:
        return True

    # Resolve the hostname to all its IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return False
    return True


def validate_service_url(service_url: str) -> str:
    """
    Validate that `service_url` points to an approved external API.

    Raises:
        ValueError: If the URL is not HTTPS, does not belong to an approved domain,
                    or resolves to a private/internal IP address.
    Returns:
        The normalized URL (scheme, host, path, query, fragment) that has been validated.
    """
    if not service_url:
        raise ValueError("Empty URL")

    parsed = urlparse(service_url)

    # Only HTTPS is allowed for external APIs
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Reject URLs with IPv4/IPv6 literals that point to private ranges
    if parsed.hostname:
        # Check for IP literal in hostname
        try:
            ip_obj = ipaddress.ip_address(parsed.hostname)
            if _is_private_ip(str(ip_obj)):
                raise ValueError("URL resolves to a private IP address")
        except ValueError:
            # Not an IP literal; validate hostname
            if not _hostname_is_allowed(parsed.hostname):
                raise ValueError(f"Hostname '{parsed.hostname}' is not allowed")

    # Normalize the URL (remove default port, strip fragments)
    netloc = parsed.hostname
    if parsed.port:
        # Preserve explicit port only if non-default (443 for https)
        if parsed.port != 443:
            netloc += f":{parsed.port}"
    normalized = urlunparse(
        (parsed.scheme, netloc, parsed.path or "/", "", parsed.query, "")
    )

    return normalized