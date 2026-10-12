import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a whitelist of allowed hostnames or domain suffixes.
WHITELIST = {
    "api.example.com",
    "public.api.service.org",
    # Allow any subdomain of trusted domain
    r"^.*\.trusted\.com$",
}

# Regular expression to detect private IP addresses (RFC1918 and loopback).
PRIVATE_IP_RE = re.compile(
    r"^(?:127\.|10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.)"
)

def _is_ip_private(host: str) -> bool:
    """Check if the host string is a private IP address."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, skip
        return False

def _is_whitelisted(host: str) -> bool:
    """Validate host against the whitelist."""
    # Direct match
    if host in WHITELIST:
        return True

    # Regex match for wildcard patterns
    for pattern in WHITELIST:
        if isinstance(pattern, str) and pattern.startswith("r"):
            # regex patterns are stored as strings with leading 'r'
            pattern = pattern[1:]
        if re.match(pattern, host):
            return True
    return False

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a secure, internal API URL.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized URL that can be safely used for internal API calls.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist or if it resolves to a private network address.
    """
    # Parse the URL
    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or network location")

    # Normalize hostname (case-insensitive)
    host = parsed.hostname.lower()

    # Reject private IP addresses
    if _is_ip_private(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Reject hosts that are not whitelisted
    if not _is_whitelisted(host):
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Rebuild a safe URL (remove fragments, query parameters if needed)
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url

# Example usage (for testing purposes only):
if __name__ == "__main__":
    try:
        print(verify_webhook("https://api.example.com/webhook"))
    except ValueError as e:
        print(f"Validation failed: {e}")