import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelist of approved public API endpoints (scheme + hostname)
WHITELIST = {
    ("https", "api.example.com"),
    ("https", "webhooks.secure.org"),
}

# Regex to detect IP addresses in the hostname part
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)   # octet
        \.
    ){3}
    (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)       # last octet
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast
    except ValueError:
        # Not a valid IP address string
        return False

def _is_allowed_host(host: str) -> bool:
    """Check if the host is in the whitelist or a valid public domain."""
    # Reject IP addresses that are private, loopback, etc.
    if IP_REGEX.match(host):
        return not _is_private_ip(host)

    # Check against domain whitelist
    for scheme, allowed_host in WHITELIST:
        if host.lower() == allowed_host.lower():
            return True
    return False

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal use.

    Parameters
    ----------
    webhook_link : str
        External webhook URL to validate.

    Returns
    -------
    str
        The validated, safe URL that can be used internally.

    Raises
    ------
    ValueError
        If the URL's domain is not whitelisted or points to a private/internal network.
    """
    if not webhook_link:
        raise ValueError("Webhook link must be a non-empty string")

    parsed = urlparse(webhook_link)

    # Ensure scheme is HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Validate host
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    if not _is_allowed_host(parsed.hostname):
        raise ValueError(f"Host '{parsed.hostname}' is not in the approved whitelist")

    # Reconstruct a clean URL (remove fragments, query parameters if needed)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url

# Example usage (uncomment to test)
# try:
#     print(validate_webhook("https://api.example.com/notify?token=abc"))
# except ValueError as e:
#     print(f"Invalid webhook: {e}")