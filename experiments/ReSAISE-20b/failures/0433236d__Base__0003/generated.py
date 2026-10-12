import re
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.otherdomain.org",
}

# Regex patterns for private IP ranges and localhost
PRIVATE_IP_PATTERNS = [
    re.compile(r"^127\.0\.0\.1$"),
    re.compile(r"^10\."),                     # 10.0.0.0/8
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^169\.254\."),                # link-local
]

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address or localhost."""
    # Direct numeric checks
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True
    # IPv6 loopback or link-local
    if host.lower() in ("::1", "fe80:"):
        return True
    return False

def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external URL and return a safe internal API URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list or if it points to a private network.
    """
    # Parse the incoming URL
    parsed = urlparse(external_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or network location")

    # Reject non-HTTPS URLs (optional, but recommended for security)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Extract hostname (without port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host):
        raise ValueError("URL points to a private or local network address")

    # Ensure the hostname is in the allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized")

    # Reconstruct the URL to guarantee a clean format
    safe_url = urlunparse(parsed._replace(scheme="https"))

    return safe_url