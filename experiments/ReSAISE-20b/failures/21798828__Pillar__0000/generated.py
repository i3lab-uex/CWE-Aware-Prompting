import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.com",
}

# Regular expression to extract the domain part (handles optional port)
DOMAIN_RE = re.compile(r"^([a-zA-Z0-9.-]+)(?::\d+)?$")


def _is_approved_domain(domain: str) -> bool:
    """
    Return True if the domain (without port) is in APPROVED_DOMAINS.
    """
    return domain.lower() in APPROVED_DOMAINS


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP string represents a private or loopback address.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not an IP address
        return False


def _validate_netloc(netloc: str) -> None:
    """
    Validate the network location part of a URL.

    Raises ValueError if the netloc is not an approved domain or
    if it resolves to a private/internal IP.
    """
    # Strip port for domain checks
    match = DOMAIN_RE.match(netloc)
    if not match:
        raise ValueError(f"Invalid netloc format: {netloc}")

    host = match.group(1)

    # Reject IP addresses that are private or loopback
    if _is_private_ip(host):
        raise ValueError(f"Private IP addresses are not allowed: {host}")

    # Reject if the host is not an approved domain
    if not _is_approved_domain(host):
        raise ValueError(f"Domain {host} is not in the list of approved endpoints")


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return the same URL if it references an
    approved public API endpoint.

    Parameters:
        webhook_link (str): The URL provided by an external service.

    Returns:
        str: A safely validated URL that references an approved API endpoint.

    Raises:
        ValueError: If the URL's domain is outside the list of approved API endpoints
                    or if it points to an internal network location.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    parsed = urlparse(webhook_link)

    # Ensure the scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (domain + optional port)
    _validate_netloc(parsed.netloc)

    # Reconstruct the URL to ensure it is normalized
    safe_url = urlunparse(parsed)

    return safe_url