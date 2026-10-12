import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define the set of approved public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.net",
}

# Regular expression for detecting IP addresses in URLs
IP_REGEX = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$|^([a-fA-F0-9:]+)$")

def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the given hostname resolves to a private or loopback IP address.
    """
    try:
        # Resolve the host name to an IP. If it's already an IP, this will succeed.
        addr = ipaddress.ip_address(hostname)
    except ValueError:
        # Not an IP, try to resolve the hostname
        try:
            import socket
            resolved = socket.gethostbyname(hostname)
            addr = ipaddress.ip_address(resolved)
        except Exception:
            # If resolution fails, treat as non-private (unknown).
            return False
    return addr.is_private or addr.is_loopback

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it if it belongs to an approved domain
    and does not point to an internal/private network.

    Args:
        webhook_address: The URL supplied by an external service.

    Returns:
        A validated URL string that can be safely used for internal API requests.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if the URL
                    points to a private/internal network.
    """
    # Parse the incoming URL
    parsed = urlparse(webhook_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or netloc")

    # Ensure the scheme is HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Extract hostname (without port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private or loopback IP addresses
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private or loopback IP address")

    # Check against allowed domains
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Reconstruct the URL to ensure no path traversal or other tampering
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://api.example.com/webhook",   # should fail (non-https)
        "https://192.168.1.10/webhook",     # should fail (private IP)
        "https://malicious.com/webhook"     # should fail (domain not allowed)
    ]

    for url in test_urls:
        try:
            print(f"Validated: {analyze_webhook(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")