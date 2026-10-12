import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelist of approved public API endpoints (domains only)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.partner.org",
    "services.thirdparty.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:                     # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or loopback address."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address; treat as not private
        return False

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized, secure URL
    that can be used for internal API calls.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A validated and secure URL ready for internal use.

    Raises
    ------
    ValueError
        If the URL domain is not in the whitelist, if it points to a private IP,
        or if the scheme is not HTTPS.
    """
    # Parse URL components
    parsed = urlparse(callback_url)

    # Scheme must be HTTPS to prevent insecure transport
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Unsupported scheme: {parsed.scheme}. HTTPS required.")

    # Resolve hostname or IP
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Reject private IP addresses
    if PRIVATE_IP_RE.match(host) or _is_private_ip(host):
        raise ValueError(f"Hostname '{host}' resolves to a private address.")

    # Enforce whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not in the approved whitelist.")

    # Reconstruct URL ensuring no path or query parameters that could alter behaviour
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        "/",  # force root path
        "",   # params
        "",   # query
        ""    # fragment
    ))

    return sanitized

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     test_url = "https://api.example.com/webhook?token=abc"
#     print(validate_callback(test_url))