import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (example values)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "public.api.service.org",
    "hooks.secure.net",
}

# Regular expression to detect IP addresses in URLs
IP_REGEX = re.compile(r"""
    ^(?P<ip>
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    )$
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private, loopback, or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host(hostname: str) -> list[str]:
    """Resolve the hostname to a list of IP addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL against an approved whitelist and
    ensure it does not resolve to any private or internal IP address.

    Parameters:
        webhook_endpoint (str): The external webhook URL to validate.

    Returns:
        str: A sanitized, validated URL that can be used for internal API calls.

    Raises:
        ValueError: If the domain is not whitelisted or resolves to a private/internal address.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Normalize hostname (lowercase, strip port)
    host = parsed.hostname.lower()
    if host is None:
        raise ValueError("URL must contain a hostname")

    # Check whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Resolve hostname to IP addresses
    ip_addresses = _resolve_host(host)

    if not ip_addresses:
        raise ValueError(f"Unable to resolve hostname '{host}'")

    # Ensure none of the resolved IPs are private/internal
    for ip in ip_addresses:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{host}' resolves to a private/internal IP address ({ip})"
            )

    # Reconstruct the URL to ensure it's in a canonical form
    sanitized_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            ""   # fragment
        )
    )

    return sanitized_url


# Example usage:
if __name__ == "__main__":
    try:
        url = verify_webhook("https://api.example.com/webhook")
        print(f"Verified URL: {url}")
    except ValueError as e:
        print(f"Verification failed: {e}")