import re
import socket
from urllib.parse import urlparse, urlunparse

# Approved public API endpoints (scheme + hostname)
WHITELIST = {
    ("https", "api.example.com"),
    ("https", "service.allowed.org"),
    # Add more allowed domains here
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|127\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r"|172\.((1[6-9])|(2\d)|(3[01]))\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []
    ips = {info[4][0] for info in infos}
    return list(ips)

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal API calls.

    Parameters
    ----------
    webhook_link : str
        External webhook URL supplied by an upstream component.

    Returns
    -------
    str
        A sanitized, validated URL that is allowed for internal API interactions.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved whitelist or if it resolves to a private/internal IP.
    """
    # Basic URL parsing
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Ensure scheme is https for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Whitelist check
    if (parsed.scheme.lower(), parsed.hostname) not in WHITELIST:
        raise ValueError("Domain is not whitelisted")

    # Resolve hostname to IPs and check for private addresses
    ips = _resolve_hostname(parsed.hostname)
    if not ips:
        raise ValueError("Could not resolve hostname")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError("URL resolves to a private/internal IP address")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed._replace(scheme="https"))
    return safe_url

# Example usage (for testing only)
if __name__ == "__main__":
    try:
        safe = validate_webhook("https://api.example.com/webhook?token=abc")
        print(f"Validated URL: {safe}")
    except ValueError as e:
        print(f"Validation error: {e}")