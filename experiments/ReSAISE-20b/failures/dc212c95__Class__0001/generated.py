import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhooks.thirdparty.io",
    "services.partner.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.0\.0\.1$)|
    (^10\.)|
    (^192\.168\.)|
    (^172\.(1[6-9]|2\d|3[01])\.)
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if the host resolves to a private IP address."""
    try:
        # Attempt to interpret as an IP address
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address; check against regex for common private patterns
        return bool(PRIVATE_IP_REGEX.search(host))

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate that a webhook URL belongs to an approved public domain
    and does not point to any private or internal network.

    Parameters:
        webhook_endpoint (str): The URL supplied by an external service.

    Returns:
        str: A sanitized and validated URL that can be safely used for
             internal API requests.

    Raises:
        ValueError: If the URL domain is not in the allowed list or
                    if it points to a private/internal network.
    """
    if not webhook_endpoint:
        raise ValueError("Webhook URL must be a non-empty string")

    parsed = urlparse(webhook_endpoint)

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or loopback IPs
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal network")

    # Ensure the host is in the list of allowed domains
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved webhook endpoint")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(parsed._replace(scheme="https"))
    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_webhook_url("https://api.example.com/webhooks/123")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Validation error: {e}")