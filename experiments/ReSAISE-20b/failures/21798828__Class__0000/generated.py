import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API domains (exact match or wildcard subdomains)
APPROVED_DOMAINS = [
    "api.example.com",
    "*.internal.example.com",  # wildcard example
]

# Regular expression to detect internal/private IP ranges
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),   # loopback
    ipaddress.ip_network("169.254.0.0/16"),# link-local
]


def _is_private_ip(host: str) -> bool:
    """Return True if host resolves to a private IP address."""
    try:
        # Attempt to parse as an IP literal
        ip = ipaddress.ip_address(host)
        return any(ip in net for net in PRIVATE_IP_RANGES)
    except ValueError:
        # Not an IP literal; assume it's a hostname and not private
        return False


def _matches_approved_domain(host: str) -> bool:
    """Check if the host matches one of the approved domains or wildcards."""
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith("*."):
            # wildcard subdomain match
            suffix = pattern[1:]  # remove '*'
            if host.endswith(suffix) and host != suffix.lstrip("*"):
                return True
        else:
            if host == pattern:
                return True
    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return a sanitized version that references
    an approved API endpoint.

    Parameters:
        webhook_link (str): The URL received from an external service.

    Returns:
        str: A validated and sanitized URL that is safe to call internally.

    Raises:
        ValueError: If the URL's domain is not approved, resolves to a private
                    network address, or uses an unsupported scheme.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    parsed = urlparse(webhook_link)

    # Only http/https are allowed
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host):
        raise ValueError(f"URL resolves to a private IP: {host}")

    # Validate against approved domains
    if not _matches_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure it doesn't contain unwanted fragments
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params,
        parsed.query,
        ""  # drop fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url