import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API endpoints (scheme+netloc)
APPROVED_ENDPOINTS = {
    "https://api.example.com",
    "https://internal.api.company.com",
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private or a loopback address."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False

def _validate_domain(parsed: urlparse) -> None:
    """Validate that the domain is in the approved list and not private."""
    # Reject schemes other than http/https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject internal or private IP addresses
    host = parsed.hostname
    if host is None:
        raise ValueError("Missing hostname")

    # If the host is an IP address, check for privacy
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        if _is_private_ip(host) or PRIVATE_IP_REGEX.match(host):
            raise ValueError(f"Private IP address detected: {host}")

    # Build the base URL (scheme + netloc) to check against approved list
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    if base_url not in APPROVED_ENDPOINTS:
        raise ValueError(f"Domain '{parsed.netloc}' is not approved")

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return the sanitized version if it points to an
    approved API endpoint.

    Parameters:
        webhook_link (str): The URL provided by the external service.

    Returns:
        str: A sanitized URL that references an approved API endpoint.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a private/internal address, or is not in the
                    approved list of endpoints.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    parsed = urlparse(webhook_link)

    # Basic sanity checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    _validate_domain(parsed)

    # Reconstruct the URL to ensure it is in a canonical form
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized

# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/notify?token=abc",
        "http://192.168.0.10/api",          # should fail
        "https://malicious.com/steal",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = handle_webhook(url)
            print(f"  → Approved URL: {result}\n")
        except ValueError as e:
            print(f"  → Rejected: {e}\n")