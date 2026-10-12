import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved public API domains (case‑insensitive)
WHITELIST_DOMAINS = {
    "api.example.com",
    "services.internal.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                                   # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}       |   # 10.0.0.0/8
        172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3} | # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3}          |   # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}      |   # 127.0.0.0/8
        ::1$                                 # IPv6 loopback
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(address: str) -> bool:
    """Return True if the address is a private or loopback IP."""
    try:
        ip = ipaddress.ip_address(address)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, not private
        return False


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API endpoints.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL to validate.

    Returns
    -------
    str
        The original, validated webhook URL if it passes all checks.

    Raises
    ------
    ValueError
        If the domain is not in the whitelist or if it resolves to a private/internal address.
    """
    # Parse the URL
    parsed = urlparse(webhook_link)

    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Separate domain and optional port
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses or loopback
    if _is_private_ip(host) or PRIVATE_IP_REGEX.match(host):
        raise ValueError(f"URL host '{host}' is a private or loopback address")

    # Check against whitelist (exact match or subdomain of allowed domain)
    if host not in WHITELIST_DOMAINS:
        # Allow subdomains of whitelisted domains
        if not any(host.endswith(f".{allowed}") for allowed in WHITELIST_DOMAINS):
            raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct the URL to ensure no hidden characters
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return cleaned