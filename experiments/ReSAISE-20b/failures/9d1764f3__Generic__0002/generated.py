import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "hooks.serviceprovider.net",
    "webhook.provider.org",
}

# Regex to detect private IP addresses in URL paths (optional)
PRIVATE_IP_PATTERN = re.compile(
    r"^(?:"
    r"(10(?:\.\d{1,3}){3})|"
    r"(172\.1[6-9](?:\.\d{1,3}){2})|"
    r"(172\.2[0-9](?:\.\d{1,3}){2})|"
    r"(172\.3[0-1](?:\.\d{1,3}){2})|"
    r"(192\.168(?:\.\d{1,3}){2})"
    r")$",
    re.IGNORECASE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private
    except ValueError:
        # Not an IP address, could be a domain name
        return False


def _is_valid_domain(domain: str) -> bool:
    """Check if the domain is in the whitelist."""
    return domain.lower() in WHITELISTED_DOMAINS


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL.

    Parameters
    ----------
    webhook_link : str
        External webhook URL to validate.

    Returns
    -------
    str
        Sanitized and validated URL ready for internal use.

    Raises
    ------
    ValueError
        If the domain is not whitelisted or points to a private network.
    """
    if not webhook_link:
        raise ValueError("Webhook URL must be a non-empty string")

    parsed = urlparse(webhook_link)

    # Enforce https scheme for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Resolve hostname (could be IP or domain)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Reject if domain not in whitelist
    if not _is_valid_domain(host):
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct URL to ensure no path traversal or query manipulation
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized