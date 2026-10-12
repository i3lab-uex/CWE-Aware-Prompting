import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API endpoints (exact hostnames)
APPROVED_HOSTS = {
    "api.example.com",
    "service.company.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)"
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host string is a private IP address or a localhost alias.
    """
    # Check for explicit IP addresses
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP, fallback to regex for common private prefixes
        return bool(PRIVATE_IP_REGEX.match(host))

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.
    
    Parameters
    ----------
    webhook_link : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints or points to an internal network location.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host):
        raise ValueError("URL points to a private or localhost address")

    # Reject if host is not in the approved list
    if host not in APPROVED_HOSTS:
        raise ValueError(f"Domain '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure it is clean
    cleaned_url = urlunparse(parsed._replace(fragment=""))
    return cleaned_url

# Example usage:
if __name__ == "__main__":
    try:
        valid = handle_webhook("https://api.example.com/webhook?token=abc")
        print(f"Validated URL: {valid}")
    except ValueError as exc:
        print(f"Validation error: {exc}")