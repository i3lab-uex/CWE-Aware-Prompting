import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "gateway.company.net",
}

# Regular expression for detecting private IP ranges
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[0-1])\.|"
    r"127\.)|^(::1$)|^fc00:|^fe80:",
    re.IGNORECASE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is a private IP address or loopback."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain is in the allowed list (case‑insensitive)."""
    return domain.lower() in ALLOWED_DOMAINS

def _validate_and_normalize(url: str) -> str:
    """Validate the URL and return a normalized version."""
    parsed = urlparse(url)

    # Must have http or https scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure a network location is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Resolve potential hostname to IPs if possible
    host = parsed.hostname

    # Reject URLs that resolve to private or loopback IPs
    try:
        # Use socket.getaddrinfo if needed; here we use ipaddress for simplicity
        if _is_private_ip(host):
            raise ValueError("URL points to a private or loopback address")
    except Exception:
        # If host is not an IP, we skip this check; DNS resolution will happen later
        pass

    # Validate the domain against the allowed list
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of allowed domains")

    # Rebuild the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(fragment=""))
    return normalized

def handle_webhook_request(external_url: str) -> str:
    """
    Process an external webhook URL and return a validated internal API URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not allowed, or if it points to a private/internal network.
    """
    return _validate_and_normalize(external_url)