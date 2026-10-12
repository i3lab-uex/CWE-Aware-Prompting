import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved domains (add or modify as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.api.net",
    "trusted.api.org",
}

# Regex for private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        # Resolve hostname to IP(s)
        for res in socket.getaddrinfo(ip, None):
            family, _, _, _, sockaddr = res
            if family == socket.AF_INET:
                addr = sockaddr[0]
                if PRIVATE_IP_REGEX.match(addr):
                    return True
    except socket.gaierror:
        # If resolution fails, treat as unsafe (most conservative)
        return True
    return False

def validate_service_url(service_url: str) -> str:
    """
    Validate that the given URL points to an approved external API.

    Args:
        service_url: The URL string to validate.

    Returns:
        A normalized URL that has been confirmed to belong to an approved domain
        and does not resolve to a private/internal address.

    Raises:
        ValueError: If the URL is malformed, not HTTPS, points to a disallowed
                    domain, or resolves to an internal/private IP.
    """
    if not isinstance(service_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(service_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Reject URLs with userinfo (e.g., http://user:pass@host)
    if parsed.username or parsed.password:
        raise ValueError("User info in URL is disallowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against approved domains (case-insensitive)
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve hostname to IPs and ensure none are private
    try:
        addrinfos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host '{host}': {exc}") from exc

    for res in addrinfos:
        family, _, _, _, sockaddr = res
        if family == socket.AF_INET:  # IPv4 only for this check
            ip = sockaddr[0]
            if PRIVATE_IP_REGEX.match(ip):
                raise ValueError(f"Host '{host}' resolves to private IP {ip}")

    # Reconstruct the URL to ensure normalization
    normalized = urlunparse(parsed._replace(fragment=""))
    return normalized

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_service_url("https://api.example.com/v1/resource")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Validation failed: {e}")