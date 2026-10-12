import re
from urllib.parse import urlparse, urlunparse

# List of approved hostnames or domain patterns
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.example.org",
}

# Regex to match private IP ranges (CWE-918 mitigation)
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (127\.0\.0\.1)|
        # IPv6 loopback and link-local
        (::1|fc00::/7|fe80::/10)
    )
    $
    """,
    re.VERBOSE,
)

def is_private_ip(host: str) -> bool:
    """Return True if host is a private IP or localhost."""
    # Handle IPv6 addresses
    if ":" in host:
        return bool(PRIVATE_IP_RE.search(host))
    # Handle IPv4
    return bool(PRIVATE_IP_RE.search(host))

def manage_webhook(url_hook: str) -> str:
    """
    Validate an external webhook URL and return it if it points to an approved API endpoint.

    Args:
        url_hook (str): The URL provided by the external service.

    Returns:
        str: The validated URL, unchanged from the input.

    Raises:
        ValueError: If the URL's domain is not approved or targets a private network.
    """
    if not isinstance(url_hook, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_hook)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses or localhost
    if is_private_ip(host):
        raise ValueError("URL points to a private or local network address")

    # Resolve hostname against approved list
    if host not in APPROVED_HOSTS:
        raise ValueError(f"Hostname '{host}' is not an approved endpoint")

    # Reconstruct URL to ensure normalization
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url

# Example usage (commented out):
# try:
#     safe = manage_webhook("https://api.example.com/webhook")
#     print(f"Safe URL: {safe}")
# except ValueError as e:
#     print(f"Validation error: {e}")