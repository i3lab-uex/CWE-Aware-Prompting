import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.allowed.org",
    "services.public.net",
}

# Regular expression to detect IPv4 or IPv6 literals in the hostname
IP_LITERAL_RE = re.compile(r"^\[?[0-9a-fA-F:.]+\]?$")

def _is_private_ip(hostname: str) -> bool:
    """
    Resolve the hostname to an IP address and check if it belongs
    to a private, loopback or link‑local range.
    """
    try:
        # Resolve all addresses for the hostname
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If resolution fails treat as invalid
        return True

    for _, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return True
        except ValueError:
            # Invalid IP address string – treat as private for safety
            return True

    return False


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL received from an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL string supplied by an external service.

    Returns
    -------
    str
        A normalized, validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private network, or uses an unapproved domain.
    """
    # Parse the URL
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain scheme and network location")

    # Ensure the URL uses HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Extract hostname (without port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Hostname could not be determined")

    # Reject URLs that contain an IP literal directly
    if IP_LITERAL_RE.match(hostname):
        raise ValueError("IP literals are not allowed in webhook URLs")

    # Resolve hostname and reject private IPs
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or loopback address")

    # Normalize the domain case for comparison
    hostname_lower = hostname.lower()

    # Check against the allowed domains list (supports subdomains)
    if not any(hostname_lower == d or hostname_lower.endswith("." + d) for d in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{hostname_lower}:{parsed.port}" if parsed.port else hostname_lower,
    )
    return urlunparse(cleaned)

# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://webhooks.allowed.org:8080/callback",
        "https://192.168.1.10/api",          # should raise
        "ftp://api.example.com/resource",    # should raise
        "https://malicious.com/evil",
    ]

    for url in test_urls:
        try:
            print(f"Valid: {validate_webhook_url(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")