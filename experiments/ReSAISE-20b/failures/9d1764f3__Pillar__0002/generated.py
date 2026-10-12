import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (example domains)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.trustedservice.org",
    "services.safe.net",
}

# Regular expression for detecting private IP ranges
PRIVATE_IP_PATTERN = re.compile(
    r"""
    ^
    (?:                     # start of group
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip_str: str) -> bool:
    """
    Determine if the given IP address string is a private or loopback address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _is_domain_whitelisted(domain: str) -> bool:
    """
    Check if the domain is in the whitelist or ends with a whitelisted domain.
    """
    return any(
        domain == wl or domain.endswith("." + wl) for wl in WHITELISTED_DOMAINS
    )


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a sanitized, secure URL
    that can be used for internal API calls.

    Parameters:
        webhook_link (str): The external webhook URL to validate.

    Returns:
        str: A sanitized URL that is safe for internal use.

    Raises:
        ValueError: If the URL domain is not in the whitelist or if it
                    attempts to resolve to a private/internal IP address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    parsed = urlparse(webhook_link)

    # Basic scheme validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Extract host (domain or IP)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Prevent DNS rebinding by resolving the host to IPs
    try:
        import socket

        resolved_ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host: {exc}") from exc

    # Check each resolved IP for private or loopback addresses
    for _, _, _, _, sockaddr in resolved_ips:
        ip_str = sockaddr[0]
        if _is_private_ip(ip_str):
            raise ValueError("URL resolves to a private or internal IP address")

    # Validate against whitelist
    if not _is_domain_whitelisted(host):
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Reconstruct the URL to ensure it contains only allowed components
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return safe_url


# Example usage (uncomment for testing)
# try:
#     print(validate_webhook("https://api.example.com/webhook"))
# except ValueError as e:
#     print(f"Invalid webhook: {e}")